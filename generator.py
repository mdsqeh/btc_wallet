from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip32Slip10Secp256k1,
    Bip84,
    Bip84Coins,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    WifEncoder
)

# 选择生成助记词还是手工输入助记词
choice = input("请选择：1. 生成新的助记词 2. 手工输入助记词 (输入1或2): ")

if choice == '1':
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(21)
    print("生成的助记词:", mnemonic)
elif choice == '2':
    mnemonic = input("请输入您的助记词（用空格分隔）: ")
else:
    raise ValueError("无效的选择，请输入1或2")

# 生成种子
seed = Bip39SeedGenerator(mnemonic).Generate()
print("种子:", seed.hex())

# 生成 BIP32 根密钥
bip32_root_key = Bip32Slip10Secp256k1.FromSeed(seed)
print("BIP32 根密钥 (xprv):", bip32_root_key.PrivateKey().ToExtended())

# 生成 BIP44 根密钥 (xprv)
bip44_root_key = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
print("BIP44 根密钥 (xprv):", bip44_root_key.PrivateKey().ToExtended())

# 派生 m/44'/0'/0' 路径的账户密钥
bip44_account_key = bip44_root_key.Purpose().Coin().Account(0)
print("派生 m/44'/0'/0' 路径的密钥 (xprv):", bip44_account_key.PrivateKey().ToExtended())
print("派生 m/44'/0'/0' 路径的公钥 (xpub):", bip44_account_key.PublicKey().ToExtended())

# 派生 m/44'/0'/0'/0 路径的扩展密钥
bip44_address_key = bip44_account_key.Change(Bip44Changes.CHAIN_EXT)
print("派生 m/44'/0'/0'/0 路径的扩展私钥 (xprv):", bip44_address_key.PrivateKey().ToExtended())
print("派生 m/44'/0'/0'/0 路径的扩展公钥 (xpub):", bip44_address_key.PublicKey().ToExtended())

# 生成 BIP84 根密钥 (zprv)
bip84_root_key = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
print("\nBIP84 根密钥 (zprv):", bip84_root_key.PrivateKey().ToExtended())

# 派生 m/84'/0'/0' 路径的账户密钥
bip84_account_key = bip84_root_key.Purpose().Coin().Account(0)
print("派生 m/84'/0'/0' 路径的密钥 (zprv):", bip84_account_key.PrivateKey().ToExtended())
print("派生 m/84'/0'/0' 路径的公钥 (zpub):", bip84_account_key.PublicKey().ToExtended())

# 派生 m/84'/0'/0'/0 路径的扩展密钥
bip84_address_key = bip84_account_key.Change(Bip44Changes.CHAIN_EXT)
print("派生 m/84'/0'/0'/0 路径的扩展私钥 (xprv):", bip84_address_key.PrivateKey().ToExtended())
print("派生 m/84'/0'/0'/0 路径的扩展公钥 (xpub):", bip84_address_key.PublicKey().ToExtended())


# 派生外部链地址 (m/44'/0'/0'/0/i)
bip44_ext_chain = bip44_account_key.Change(Bip44Changes.CHAIN_EXT)
num_addresses = int(input("请输入要生成的地址数量: "))
print("\nBIP44 地址派生 (Legacy P2PKH):")
for i in range(num_addresses):
    address_key = bip44_ext_chain.AddressIndex(i)
    wif_priv_key = WifEncoder.Encode(address_key.PrivateKey().Raw().ToBytes())
    # 使用压缩格式的非扩展公钥
    raw_pub_key = address_key.PublicKey().RawCompressed().ToHex()
    print(f"索引 {i}:")
    print(f"  私钥 (WIF): {wif_priv_key}")
    print(f"  公钥 (压缩): {raw_pub_key}")
    print(f"  地址: {address_key.PublicKey().ToAddress()}")



# 派生外部链地址 (m/84'/0'/0'/0/i)
bip84_ext_chain = bip84_account_key.Change(Bip44Changes.CHAIN_EXT)
print("\nBIP84 地址派生 (Native SegWit P2WPKH):")
for i in range(num_addresses):
    address_key = bip84_ext_chain.AddressIndex(i)
    wif_priv_key = WifEncoder.Encode(address_key.PrivateKey().Raw().ToBytes())
    # 使用压缩格式的非扩展公钥
    raw_pub_key = address_key.PublicKey().RawCompressed().ToHex()
    print(f"索引 {i}:")
    print(f"  私钥 (WIF): {wif_priv_key}")
    print(f"  公钥 (压缩): {raw_pub_key}")
    print(f"  地址: {address_key.PublicKey().ToAddress()}")
