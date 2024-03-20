import os

from pyfbsdk import FBComponent, FBFindObjectByFullName, FBSystem, FBFileReference


def _load(file_path: str):
    _, file_name = os.path.split(file_path)
    ref_name = file_name.split(".")[0]
    FBSystem().Scene.NamespaceImport(ref_name, file_path, True)

    return ref_name


def _get_by_name(ref_name: str):
    return FBFindObjectByFullName(f"FileReference::{ref_name}")


def load(file_path: str):
    ref_name = _load(file_path)
    reference = _get_by_name(ref_name)
    if not reference:
        raise RuntimeError("Error on import reference !")
    
    return reference


def remove(ref: FBFileReference):
    ref.IsLoaded = False
    ref.FBDelete()


def reload(ref: FBFileReference):
    file_path = ref.ReferenceFilePath
    remove(ref)

    return load(file_path)


def get_all():
    referenced_files = []

    scene = FBSystem().Scene
    if not scene:
        return referenced_files

    for i in range(scene.GetSrcCount()):
        src = scene.GetSrc(i)
        if isinstance(src, FBComponent) and src.ClassName() == "FBFileReference":
            referenced_files.append(_get_by_name(src.LongName))

    return referenced_files
