import algosdk as sdk
import algokit_utils as au
import client as cl

algorand = au.AlgorandClient.from_environment()

code = "pioneer road rug owner lava slogan whale atom ramp motion oak execute snow mirror sight squirrel toward mention adjust become grape ridge basic abstract able"

account = algorand.account.from_mnemonic(mnemonic=code)
public_address = account.address

account_manager = au.AccountManager(algorand.client)
algorand.account.ensure_funded(account, account_manager.dispenser_from_environment(), min_spending_balance=1_000_000)

try:
    factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory, default_sender=public_address
    )

    result, _ = factory.send.create.bare()
    app_id = result.app_id

    ac = factory.get_app_client_by_id(app_id, default_sender=public_address)
except sdk.error.AlgodHTTPError as e:
    if e.code == 400 and e.message == "Application already exists":
        app_id = 1
        ac = factory.get_app_client_by_id(app_id, default_sender=public_address)
    else:
        raise

box_key = public_address

args = cl.AddStudentsArgs(account=public_address)

param = au.CommonAppCallParams(box_references=[box_key])

ac.send.claim_algo(param)

ac.send.add_students(args, param)