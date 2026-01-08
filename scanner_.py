import subprocess

def get_command_output(command):
 
    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True, 
            check=True   )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}:")
        print(e.stderr)
        return None


def get_scanner():
    output = get_command_output("netsh wlan show networks")
    if output:
        print("Output from command:")
        p_data=output.split('\n')
    networks=[]
    for p in p_data:
        if "SSID" in p:
            networks.append(p.split(':')[1])
    print(networks)
    return networks