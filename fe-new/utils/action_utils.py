from actions import InstallAction

def npm_install_action(*packages: str) -> InstallAction:
    return InstallAction(["npm", "install", *packages])