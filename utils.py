import os
from pathlib import Path
import json
from . import constants
import bpy

def find_models(directory):
    formats = ['.fbx', '.obj', '.abc']

    models = list()

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        filename, file_extension = os.path.splitext(path)
        if file_extension in formats:
            models.append(path)

    return models

def ends_with(file, suffixes):
    name = Path(file).stem

    for suffix in suffixes:
        if name.lower().endswith(suffix.lower()):
            return True
    return False

def is_roughness(file):
    
    if ends_with(file, ["roughness", "_r"]):
        return True

    return False

def is_albedo(file):
    if ends_with(file, ["color", "colour", "diffuse", "albedo", "_c", "-c"]):
        return True

    return False

def is_metallic(file):
    if ends_with(file, ["metal", "metalness", "metallic", "_m", "-m"]):
        return True

    return False

def is_displacement(file):
    if ends_with(file, ['displacement']):
        return True

    return False

def is_normal(file):
    if ends_with(file, ['normal', 'normalgl']):
        return True

    return False

def is_dx_normal(file):
    if ends_with(file, ['normaldx']):
        return True

    return False

def is_ambient_occlusion(file):
    if ends_with(file, ['_ao', '-ao' 'ambientocclusion', "ambient_occlusion" ]):
        return True
    return False

def is_preview(file):
    if ends_with(file, ['preview', "prev", "thumb", "thumbnail"]):
        return True
    return False

def classify_texture(file):

    if is_roughness(file):
        return constants.roughness

    if is_metallic(file):
        return constants.metallic

    if is_albedo(file):
        return constants.albedo

    if is_ambient_occlusion(file):
        return constants.ambient_occlusion

    if is_normal(file):
        return constants.normal

    if is_dx_normal(file):
        return constants.normal_dx

    if is_displacement(file):
        return constants.displacement

    if is_preview(file):
        return constants.preview

    return None

def find_textures(directory):
    formats = ['.png', '.jpg', '.jpeg', '.exr', '.tiff']

    images = dict()

    for file in os.listdir(directory):

        path = os.path.join(directory, file)

        if os.path.isdir(path):
            continue

        filename, file_extension = os.path.splitext(path)
        if not file_extension in formats:
            continue

        type = classify_texture(path)

        if type == None:
            continue

        images[type] = path

    return images

def find_tags_json(json_file):
    f = open(json_file)
  
    data = json.load(f)

    keys = ['tags', "TAGS", "Tags"]

    for key in keys:
        if key in data:
            print(list(data[key]))
            tags = list(data[key])
            return tags

def find_tags(directory):

    tags = list()
    for file in os.listdir(directory):
        path = os.path.join(directory, file) 

        if path.endswith(".json"):
            json_tags = find_tags_json(path)
            if json_tags == None:
                continue
            
            tags = tags + json_tags

    return tags

def find_name_json(json_file):
    f = open(json_file)
  
    data = json.load(f)

    keys = ['name', "NAME", "Name"]

    for key in keys:
        if key in data:
            return str(data[key])

    return None

def find_name(directory):

    name = None

    for file in os.listdir(directory):
        path = os.path.join(directory, file) 

        if path.endswith(".json"):
            name_json = find_name_json(path)
            if name_json != None:
                return name_json

def find_asset(directory):
    models = find_models(directory)
    textures = find_textures(directory)

    asset = dict()

    if len(models) > 0:
        asset[constants.models] = models

    if len(textures) > 0:
        asset[constants.textures] = textures

    if len(asset.keys()) == 0:
        return None

    tags = find_tags(directory)

    name = find_name(directory)

    if len(tags) > 0:
        asset[constants.tags] = tags

    if name is not None:
        asset[constants.name] = name

    return asset

def find_assets(directory):

    assets = list()

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if not os.path.isdir(path):
            continue

        asset = find_asset(path)
        if asset is not None:
            assets.append(asset)
        assets = assets + find_assets(path)

    return assets


def get_asset_name(asset):

    if constants.name in asset:
        return asset[constants.name]

    if constants.models in asset:
        return Path(asset[constants.models][0]).stem

    textures = asset[constants.textures]
    texture = textures[list(textures)[0]]

    name = Path(texture).stem

    if name.count("_") > 1:
        name = name.rpartition("_")[0]

    return name

color_textures = [constants.albedo]
def create_material(textures, template_material, name):
    print("Creating Material: " + name)
    material = template_material.copy()
    material.name = name

    for texture in textures:
        print("Attempting to load: " + texture)

        if not texture in material.node_tree.nodes:
            print("No Node Found")
            continue

        node = material.node_tree.nodes[texture]
        if node.type != constants.texture_node:
            print("Node type incorrect")
            continue

        node.image = bpy.data.images.load(textures[texture])

        if texture not in color_textures:
            node.image.colorspace_settings.name = 'Non-Color'

        print("Loaded Image")
    
    return material

def import_assets(assets, template_material_name):

    template_material = bpy.data.materials[template_material_name]

    for asset in assets:

        print("Creating Asset: ")
        print(json.dumps(asset, indent=4))
        print("")


        name = get_asset_name(asset)

        if constants.textures in asset:
            material = create_material(asset[constants.textures], template_material, name)

        if constants.models in asset:
            pass