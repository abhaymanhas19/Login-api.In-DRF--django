import json


# def main():
#     with open('data.json', '+r') as f:
#         file_data = f.read()
#         file_data = json.loads(file_data)
#         processed_json = []
#         with open('new_data.json', '+w') as wf:
#             for i in file_data:
#                 if i['model']=='dna.provnotification':
#                     i["fields"]["message"] = json.dumps(i["fields"]["message"])
#                 processed_json.append(i)
#             wf.write(json.dumps(processed_json, indent=4))
def replace_customer():
    with open("customer.json", "+r") as f:
        file_data = f.read()
        file_data = json.loads(file_data)
        processed_json = []
        with open("organization.json", "+w") as wf:
            for i in file_data:
                if i["model"] == "customer.customer":
                    i["fields"]["message"] = json.dumps(i["fields"]["message"])
                processed_json.append(i)
            wf.write(json.dumps(processed_json, indent=4))


def split_mobile_dna():
    with open("raw/data4.json", "+r") as f:
        file_data = f.read()
        file_data = json.loads(file_data)   
        mobile = []
        dna = []
        for i in file_data:
            if "mobile." in i["model"]:
                mobile.append(i)
            if "dna." in i["model"]:
                dna.append(i)
        with open("dna.json", "+w") as dna_f:
            dna_f.write(json.dumps(dna, indent=4))
        with open("mobile.json", "+w") as mob_f:
            mob_f.write(json.dumps(mobile, indent=4))


if __name__ == "__main__":
    # main()
    # replace_customer()
    split_mobile_dna()
