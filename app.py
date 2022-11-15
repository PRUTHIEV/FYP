from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from DB import authenticate_user, insert_record
from Ipfs import ipfs_upload
from web3 import Web3
from Web3.deploy import compile_solidity
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
db = SQLAlchemy(app)
app.config["IMAGE_UPLOADS"] = "./static/img"


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.String(length=60), nullable=False)

    def __repr__(self) -> str:
        return f"Username {self.username} Email {self.email} password {self.password}"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        byte_name_arr = ""
        for char in str(request.form["username"]):
            byte_name_arr += str(ord(char))
        print(byte_name_arr)
        print(
            request.form["username"],
            request.form["password"],
            str(request.form["username"]) + str(request.form["password"]),
        )
        data = authenticate_user(
            str(request.form["username"]), str(request.form["password"])
        )
        if len(data) == 0:
            return render_template("login.html", error="Incorret Username or Password")
        return render_template("skin_form.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form)
        byte_name_arr = ""
        for char in str(request.form["name"]):
            byte_name_arr += str(ord(char))
        print(byte_name_arr)
        insert_record(
            username=str(request.form["name"]),
            password=request.form["password"],
            email=request.form["email"],
        )
        return "post registered"
    else:
        return "Registered"


def get_abi_bytecode():
    with open("./compiled_code.json", "r") as j:
        json_data = json.loads(j.read())
    ABI = json_data["contracts"]["Patient.sol"]["Patient"]["abi"]
    BYTECODE = json_data["contracts"]["Patient.sol"]["Patient"]["evm"]["bytecode"][
        "object"
    ]
    return ABI, BYTECODE


def add_patient_block(
    phone_number,
    age,
    bloog_grp,
    blood_pressure,
    skin_img_ipfs_hash,
    date,
    time,
    state,
    city,
):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0x7f21EF7f1185aA02fb597B7F77C1255E27137B63"
    private_key = "0xf8c8ab49ddd90558a152e48a925c42a4b41a8a2ed7b3f1d5f6446f960938eb0a"
    ABI, BYTECODE = get_abi_bytecode()
    PatientContract = w3.eth.contract(abi=ABI, bytecode=BYTECODE)
    nonce = w3.eth.getTransactionCount(my_address)
    PatientTransaction = PatientContract.constructor(
        phone_number,
        age,
        skin_img_ipfs_hash,
        bloog_grp,
        blood_pressure,
        date,
        time,
        state,
        city,
    ).build_transaction(
        {
            "gasPrice": w3.eth.gas_price,  # Remove the gas price field once it is deployed on the real ethereum network
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
        }
    )
    sign_transaction = w3.eth.account.sign_transaction(
        PatientTransaction, private_key=private_key
    )
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return ABI, nonce, transaction_receipt.contractAddress


def retrieve_patient_block(contract_address, ABI):
    print(f"Retrieving the block at {contract_address} address")
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    PatientBlock = w3.eth.contract(address=str(contract_address), abi=ABI)
    print(f"Patient Blood Group {PatientBlock.functions.getBloodGroup().call()}")
    print(f"Patient Blood Pressure {PatientBlock.functions.getBloodPressure().call()}")
    print(f"Patient Phone Number {PatientBlock.functions.getPhoneNumber().call()}")
    print(
        f"Patient Skin Image IPFS {PatientBlock.functions.getSkinDiseaseIpfs().call()}"
    )
    print(f"Patient Appointment Date {PatientBlock.functions.getDate().call()}")
    print(f"Patient Appointment Time {PatientBlock.functions.getTime().call()}")
    print(f"Patient State {PatientBlock.functions.getState().call()}")
    print(f"Patient city {PatientBlock.functions.getCity().call()}")


@app.route("/skin_consult", methods=["GET", "POST"])
def skin_consult():
    if request.method == "POST":
        print(request.form)
        img = request.files["img"]
        path_save = "./static/img/Patients/Skin/" + img.filename
        img.save(path_save)
        ABI, nonce, contract_address = add_patient_block(
            str(request.form["ph_no"]),
            str(request.form["age"]),
            str(request.form["bd_grp"]),
            str(request.form["bd_prs"]),
            str(ipfs_upload(path_save)),
            str(request.form["date"]),
            str(request.form["time"]),
            str(request.form["state"]),
            str(request.form["city"]),
        )
        print("Adding a new block ...")
        print(f"The new block number is {nonce}")
        print(f"The contract address {contract_address}")
        retrieve_patient_block(contract_address, ABI)
        return "posted"
    else:
        return render_template("skin_form.html")


if __name__ == "__main__":
    app.run(debug=True)
