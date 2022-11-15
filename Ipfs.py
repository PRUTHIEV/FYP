from pinata import Pinata
from urllib import request
from flask import request as req
import json

def ipfs_retrieve():
    ipfs_api_endpoint = "https://gateway.pinata.cloud/ipfs/"
    ipfs_hash = "QmRQXjY5fGQX8gnt3iU88uqsWNaYgYfnHGSNFecPcQ5DSy"
    opener = request.URLopener()
    opener.addheader("User-Agent", "chrome")
    opener.retrieve(
        ipfs_api_endpoint + ipfs_hash,
        "file.jpg",
    )


def ipfs_upload(file):
    api_key = "4c15d0104ee38cdc7902"
    secret_key = "a565ea8c1cdfe2389e9450de79366398831da3973d244fdc41881ca21fc25a6e"
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwZmYxZTcxMy05NWY0LTQ4NjAtYmEzOC04MmM2ZDY2YTNlMjkiLCJlbWFpbCI6ImFzcHJ1dGhpZXZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjRjMTVkMDEwNGVlMzhjZGM3OTAyIiwic2NvcGVkS2V5U2VjcmV0IjoiYTU2NWVhOGMxY2RmZTIzODllOTQ1MGRlNzkzNjYzOTg4MzFkYTM5NzNkMjQ0ZmRjNDE4ODFjYTIxZmMyNWE2ZSIsImlhdCI6MTY2ODA2Mzk1M30.VGmG81-niHz7ZkBHXrxVS6-VjkGpnZEz7G__0OK8Rlw"
    pinata = Pinata(api_key, secret_key, access_token)
    return pinata.pin_file(file)["data"]["IpfsHash"]


if __name__ == "__main__":
    ipfs_upload()
