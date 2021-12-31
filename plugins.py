import importlib
import os

PluginFolder = "./plugins"
MainModule = "__init__"

def getPlugins():
    plugins = []
    reqs = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        if "requirements.txt" in os.listdir(location):
            requirements = os.path.join(location, "requirements.txt")
            with open(requirements, "r") as f:
                requirements = f.read().splitlines()
            reqs.append(requirements)
        info = importlib.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def loadPlugin(plugin):
    return importlib.load_module(MainModule, *plugin["info"])