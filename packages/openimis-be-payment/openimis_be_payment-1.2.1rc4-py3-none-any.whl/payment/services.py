import logging
from gettext import gettext as _

from contribution.models import Premium
from django.db import connection, transaction
from django.db.models import OuterRef, Sum, Exists
from insuree.models import Insuree
from payment.models import Payment, PaymentDetail
from policy.models import Policy
from product.models import Product

logger = logging.getLogger(__file__)


def set_payment_deleted(payment):
    try:
        for pd in payment.payment_details.filter(validity_to__isnull=True):
            pd.delete_history()
        payment.delete_history()
        return []
    except Exception as exc:
        logger.debug("Exception when deleting payment %s", payment.uuid, exc_info=exc)
        return {
            'title': payment.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_delete_payment") % {'uuid': payment.uuid},
                'detail': payment.uuid}]
        }


def detach_payment_detail(payment_detail):
    try:
        payment_detail.save_history()
        payment_detail.premium = None
        payment_detail.save()
        return []
    except Exception as exc:
        return [{
            'title': payment_detail.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_detach_payment_detail") % {'payment_detail': str(payment_detail)},
                'detail': payment_detail.uuid}]
        }]


def reset_payment_before_update(payment):
    payment.expected_amount = None
    payment.received_amount = None
    payment.officer_code = None
    payment.phone_number = None
    payment.request_date = None
    payment.received_date = None
    payment.status = None
    payment.transaction_no = None
    payment.origin = None
    payment.matched_date = None
    payment.receipt_no = None
    payment.payment_date = None
    payment.rejected_reason = None
    payment.date_last_sms = None
    payment.language_name = None
    payment.type_of_payment = None
    payment.transfer_fee = None


def update_or_create_payment(data, user):
    if "client_mutation_id" in data:
        data.pop('client_mutation_id')
    if "client_mutation_label" in data:
        data.pop('client_mutation_label')
    from core import datetime
    now = datetime.datetime.now()
    # No audit here
    # data['audit_user_id'] = user.id_for_audit
    data.pop("rejected_reason", None)
    data['validity_from'] = now
    payment_uuid = data.pop("uuid") if "uuid" in data else None
    if payment_uuid:
        payment = Payment.objects.get(uuid=payment_uuid)
        payment.save_history()
        reset_payment_before_update(payment)
        [setattr(payment, k, v) for k, v in data.items()]
        payment.save()
    else:
        payment = Payment.objects.create(**data)
    return payment


def update_or_create_payment_detail(payment, premium_uuid, user):
    premium = Premium.filter_queryset()\
        .filter(uuid=premium_uuid)\
        .select_related("policy__family__head_insuree")\
        .select_related("policy__product")\
        .filter(policy__validity_to__isnull=True)\
        .filter(policy__product__validity_to__isnull=True)\
        .filter(policy__family__validity_to__isnull=True)\
        .filter(policy__family__head_insuree__validity_to__isnull=True)\
        .values("id",
                "amount",
                "policy__stage",
                "policy__enroll_date",
                "policy__family__head_insuree__chf_id",
                "policy__product__code")\
        .first()
    payment_detail, _ = PaymentDetail.objects.update_or_create(
        payment=payment, premium_id=premium["id"],
        defaults=dict(
            audit_user_id=user.id_for_audit,
            amount=payment.received_amount,
            product_code=premium["policy__product__code"],
            insurance_number=premium["policy__family__head_insuree__chf_id"],
            policy_stage=premium["policy__stage"],
            enrollment_date=premium["policy__enroll_date"],
            expected_amount=premium["amount"],
        )
    )
    return payment_detail


def legacy_match_payment(payment_id=None, audit_user_id=-1):
    with connection.cursor() as cur:
        sql = """
            SET NOCOUNT ON;
            DECLARE @ret int;
            EXEC @ret = [dbo].[uspMatchPayment] @PaymentID = %s, @AuditUserId = %s;
            SELECT @ret;
        """
        cur.execute(sql, (payment_id, audit_user_id,))

        if cur.description is None:  # 0 is considered as 'no result' by pyodbc
            res = None
        else:
            res = cur.fetchone()[0]  # FETCH 'SELECT @ret' returned value
        if cur.nextset() and cur.description:
            additional_response = cur.fetchall()
            logger.debug("Additional response from uspMatchPayment: %s", additional_response)
        if res:
            raise Exception(res)


def match_payment_no_raw(payment_id=None, audit_user_id=-1):
    if payment_id:
        payment = Payment.filter_queryset().get(id=payment_id)

    # TODO: not sure about the OuterRef here, we are checking what is already paid by what exactly ?
    # The existing code (recently updated) sums the entire table
    already_paid = PaymentDetail.filter_queryset().filter(payment__matched_date__isnull=False)\
        .filter(payment_id=OuterRef("payment_id"))\
        .values(already_paid=Sum("amount"))
    valid_insuree = Insuree.filter_queryset()\
        .filter(chf_id=OuterRef("insurance_number"))
    valid_product = Product.filter_queryset()\
        .filter(code=OuterRef("product_code"))
    policy = Policy.filter_queryset().exclude(status__in=[Policy.STATUS_SUSPENDED, Policy.STATUS_EXPIRED])\
        .filter(product__code=OuterRef("product_code"))\
        .filter(family__members__chf_id=OuterRef("insurance_number"))

    pd_queryset = PaymentDetail.filter_queryset().filter(premium_id__isnull=True)\
        .filter(payment__status=Payment.STATUS_UNMATCHED)\
        .filter(payment__status=Payment.STATUS_UNMATCHED)\
        .annotate(already_paid=already_paid)\
        .annotate(valid_insuree=Exists(valid_insuree))\
        .annotate(valid_product=Exists(valid_product))\
        .annotate(policy_id=policy.values("id"))

    if payment_id:
        pd_queryset = pd_queryset.filter(payment_id=payment_id)

    nb_missing_insurance_number = 0
    nb_missing_product_code = 0
    nb_missing_insuree = 0
    nb_missing_product = 0
    for pd in pd_queryset:
        # Validate and fetch insuree/policy/product/...
        if not pd.insurance_number:
            nb_missing_insurance_number += 1
            continue

        if not pd.product_code:
            nb_missing_product_code += 1
            continue

        if not pd.valid_insuree:
            nb_missing_insuree += 1
            continue

        if not pd.valid_product:
            nb_missing_product += 1
            continue

TBLDETAIL_DEF = f"""
CREATE TABLE #tblDetail
(
   PaymentDetailsID  BIGINT,
   PaymentID         BIGINT,
   InsuranceNumber   nvarchar(12),
   ProductCode       nvarchar(8),
   EnrollDate    DATE,
   PolicyStage       CHAR(1),
   MatchedDate       DATE, --
   PolicyValue       DECIMAL(18, 2),
   DistributedValue  DECIMAL(18, 2), --
   policyID          INT,
   RenewalPolicyID   INT, -- unused ?
   PremiumID         INT,
   PolicyStatus      INT,
   AlreadyPaidDValue DECIMAL(18, 2)
)
"""


TBLDETAIL_QUERY = f"""
SELECT PD.PaymentDetailsID,
        PY.PaymentID,
        PD.InsuranceNumber,
        PD.ProductCode,
        PL.EnrollDate,
        PD.PolicyStage,
        null as MatchedDate,
        PL.PolicyValue,
        null as Distributedvalue,
        PL.PolicyID,
        null as RenewalPolicyID,
        PRM.PremiumId,
        PL.PolicyStatus,
        (SELECT SUM(PDD.Amount)
         FROM tblPaymentDetails PDD
                  INNER JOIN tblPayment PYY ON PDD.PaymentID = PYY.PaymentID
         WHERE PYY.MatchedDate IS NOT NULL
           and PDD.ValidityTo is NULL)     AlreadyPaidDValue
 INTO #tblDetail
 FROM tblPaymentDetails PD
          LEFT OUTER JOIN tblInsuree I ON I.CHFID = PD.InsuranceNumber
          LEFT OUTER JOIN tblFamilies F ON F.FamilyID = I.FamilyID
          LEFT OUTER JOIN tblProduct PR ON PR.ProductCode = PD.ProductCode
          LEFT OUTER JOIN (SELECT PolicyID, EnrollDate, PolicyValue, FamilyID, ProdID, PolicyStatus
                           FROM tblPolicy
                           WHERE ValidityTo IS NULL
                             AND PolicyStatus NOT IN ({Policy.STATUS_SUSPENDED}, {Policy.STATUS_EXPIRED})) PL
                          ON PL.ProdID = PR.ProdID AND PL.FamilyID = I.FamilyID
          LEFT OUTER JOIN (SELECT MAX(PremiumId) PremiumId, PolicyID
                           FROM tblPremium
                           WHERE ValidityTo IS NULL
                           GROUP BY PolicyID) PRM ON PRM.PolicyID = PL.PolicyID
          INNER JOIN tblPayment PY ON PY.PaymentID = PD.PaymentID
 WHERE PD.PremiumID IS NULL
   AND PD.ValidityTo IS NULL
   AND I.ValidityTo IS NULL
   AND PR.ValidityTo IS NULL
   AND F.ValidityTo IS NULL
   AND PY.ValidityTo IS NULL
   AND PY.PaymentStatus = {Payment.STATUS_UNMATCHED}
   AND PD.PaymentID = ISNULL(%s, PD.PaymentID)
"""

@transaction.atomic
def match_payment(payment_id=None, audit_user_id=-1):
    if payment_id:
        payment = Payment.filter_queryset().get(id=payment_id)

    with connection.cursor() as cur:
        cur.execute(TBLDETAIL_DEF)
        cur.execute(TBLDETAIL_QUERY, (payment_id,))
        cur.execute("select * from #tblDetail;")
        foo=cur.fetchall()


