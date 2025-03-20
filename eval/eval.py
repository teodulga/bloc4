import algosdk as sdk
import algokit_utils as au
import client as cl
import algokit_utils.transactions.transaction_composer as att

# def account_creation(algorand: au.AlgorandClient, name: str, funds=au.AlgoAmount(algo=0)):
#     account = algorand.account.from_environment(name, fund_with=funds)
#     info = algorand.client.algod.account_info(account.address)
#     print(
#         f"Name\t\t: %s \n"
#         f"Address\t\t: %s\n"
#         f"Created Asset\t: %s\n"
#         f"Assets\t\t: %s\n"
#         f"Algo\t\t: %.6f"
#         % (
#             name,
#             account.address,
#             info["created-assets"],
#             info["assets"],
#             info["amount"] / 1_000_000,
#         )
#     )
#     if len(info["created-apps"]) > 0:
#         print(f"Created-Apps\t: %s \n" % info["created-apps"][0]["id"])
#     print("")
#     return account

algorand = au.AlgorandClient.testnet()

code = "pioneer road rug owner lava slogan whale atom ramp motion oak execute snow mirror sight squirrel toward mention adjust become grape ridge basic abstract able"

account = algorand.account.from_mnemonic(mnemonic=code)

# alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10000))

eval_factory = cl.EvalFactory(
    algorand=algorand,
    default_sender=account.address,
)

app_id = 736038676


ac = eval_factory.get_app_client_by_id(app_id, default_sender=account.address, default_signer=account.signer)

# algorand.account.ensure_funded(account, alice, min_spending_balance=au.AlgoAmount(micro_algo=1_000_000), min_funding_increment=au.AlgoAmount(micro_algo=1_000_000))
# algorand.account.ensure_funded(ac.app_address, alice, min_spending_balance=au.AlgoAmount(micro_algo=1_000_000), min_funding_increment=au.AlgoAmount(micro_algo=1_000_000))

box_key = account.public_key

# args = cl.AddStudentsArgs(account=account.address)

# param = au.CommonAppCallParams(box_references=[box_key])

# ac.send.add_students(args, param)

# q1 = b"q1" + box_key

# param = au.CommonAppCallParams(box_references=[box_key, q1])

# ac.send.claim_algo(param)

result = algorand.send.asset_create(
        au.AssetCreateParams(
            sender=account.address,
            signer=account.signer,
            total=15,
            decimals=0,
            default_frozen=False,
            unit_name="PY-CL-FD",
            asset_name="Proof of Attendance Py-Clermont",
            url="https://pyclermont.org/",
            note="Hello Clermont",
        )
    )
asset_id = result.confirmation["asset-index"]

mbr_pay_txn = algorand.create_transaction.payment(
        au.PaymentParams(
            sender=account.address,
            receiver=ac.app_address,
            amount=au.AlgoAmount(algo=0.2),
            extra_fee=au.AlgoAmount(micro_algo=1_000),
        )
    )

args = cl.OptInToAssetArgs(
    mbr_pay=att.TransactionWithSigner(mbr_pay_txn, account.signer),
    asset=asset_id,
)

q2 = b"q2" + box_key

param = au.CommonAppCallParams(box_references=[box_key, q2])

ac.send.opt_in_to_asset(args, param)

q3 = b"q3" + box_key

array = [1, 2]
byte_array = bytes(array)

args = cl.SumArgs(array=byte_array)

param = au.CommonAppCallParams(box_references=[box_key, q3])

ac.send.sum(args, param)

q4 = b"q4" + box_key

args = cl.UpdateBoxArgs(value="Hello")

param = au.CommonAppCallParams(box_references=[box_key, q4])

ac.send.update_box(args, param)