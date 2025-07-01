import subprocess
import time
import json
import os

# ← あなたのスマホのBluetooth MACアドレスをここに
#setting current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#setting parent directory
parent_dir = os.path.dirname(current_dir)
#jsonファイルの読み込み
with open(os.path.join(parent_dir, 'setting/member.json'), 'r') as f:
    data = json.load(f)
    TARGET_MAC = data['test22']['mac']


def is_device_nearby(mac):
    """hcitoolで近くにあるデバイスにそのMACアドレスがあるか確認"""
    try:
        output = subprocess.check_output("hcitool scan", shell=True).decode()
        return mac in output
    except Exception:
        return False

def connect_device(mac):
    """bluetoothctl を使ってペアリング・信頼・接続する"""
    cmds = [
        'power on',
        'agent on',
        'default-agent',
        f'pair {mac}',
        f'trust {mac}',
        f'connect {mac}'
    ]
    print(f"→ デバイス {mac} に接続します")
    process = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for cmd in cmds:
        process.stdin.write((cmd + '\n').encode('utf-8'))
        time.sleep(1.5)
    process.stdin.write(b'exit\n')
    out, _ = process.communicate()
    print(out.decode())

def main():
    print("🔍 デバイス探索中...")
    print(f"ターゲットMAC: {TARGET_MAC}")
    while True:
        if is_device_nearby(TARGET_MAC):
            print("✅ デバイス検出！接続を試みます...")
            connect_device(TARGET_MAC)
            break
        else:
            print("…見つかりません。再試行します。")
            time.sleep(5)

if __name__ == "__main__":
    main()
