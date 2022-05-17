# Masset
### Mass asset importer for blender
---
Masset is a plugin designed to import large amounts of assets automatically, by analysing the files of a given directory

Currently it has support for PBR texture sets

### Material Setup
Masset allows you to configure custom shaders to be used for the asset import. To use this, create a base material, and add 'Image Texture' nodes, with names: `albedo`, `roughness`, `metallic`, `displacement`, `normal`, `ambient_occlusion`

When selecting a folder to import, insert the name of this base material in the `Template Material` setting.

If everything is configured correctly, Masset will create copies of this material, and insert the corresponding textures. 

Note: It may be a good idea to create a Node Group which takes the textures as inputs, and a shader as the output. Since when the materials are copied, this node group remains linked between each material. This will allow you to modify the shader after import, and have all changes automatically apply to every imported material

### Asset Browser

There is a `Mark as Asset` checkbox. If this is enabled, all assets that are imported will be automatically marked as an asset for the Blender asset browser, and preview thumbnails will be automatically generated. If Masset was able to find any data for tags, those will also be added.

### Ignore Regex

This optional setting allows for an input of a Regular Expression, which if the path of a file/folder in the directory matches, this file/folder will be ignored.