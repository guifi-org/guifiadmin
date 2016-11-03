# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA

from . import vpn_settings


def generate_RSA(bits=vpn_settings.RSA_BITS):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    new_key = RSA.generate(bits)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key
