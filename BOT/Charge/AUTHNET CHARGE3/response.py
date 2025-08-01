
import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *

async def get_charge_resp(result: str, user_id: int, fullcc: str) -> dict:
    try:
        if isinstance(result, str):
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            code_text = result
            hits = "NO"

            if '{"resultCode":"Ok","messageCode":"Ok"' in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Payment Successfull"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif '{"resultCode":"Error","messageCode":"2","messageText":"This transaction has been declined.' in result:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "This transaction has been declined."
                hits = "NO"

            elif "An error occurred during processing. Call Merchant Service Provider" in result:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "An error occurred during processing. Call Merchant Service Provider"
                hits = "NO"

            elif "A duplicate transaction has been detected." in result:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "A duplicate transaction has been detected."
                hits = "NO"

            elif '{"resultCode": "Ok", "messageCode": "1"' in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "Payment Successfull"
                hits = "YES"

            elif '{"resultCode":"Error","messageCode":"8","messageText":"The credit card has expired.' in result:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "The credit card has expired."
                hits = "NO"

            elif ("We're sorry, but the payment validation failed. Declined - Call Issuer" in result or 
                   "Payment failed: Declined - Call Issuer" in result):
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "Declined - Call Issuer"
                hits = "NO"

            elif "ProxyError" in result:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                response = "Proxy Connection Refused"
                hits = "NO"
                await refundcredit(user_id)

            else:
                status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                try:
                    response = result.split('"message": "')[1].split('"')[0] + " ❌"
                except:
                    response = result
                await result_logs(fullcc, "Braintree Auth", result)
                hits = "NO"

            json = {
                "status": status,
                "response": response,
                "hits": hits,
                "fullz": fullcc,
            }
            return json

        else:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response = str(result) + " ❌"
            hits = "NO"
            json = {
                "status": status,
                "response": response,
                "hits": hits,
                "fullz": fullcc,
            }
            return json

    except Exception as e:
        traceback.print_exc()
        status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = str(e) + " ❌"
        hits = "NO"
        json = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json
