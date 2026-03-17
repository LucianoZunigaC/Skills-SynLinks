from itertools import groupby
from typing import List

from src.features.packages.config import DEFAULT_GROUP_ID, DEFAULT_GROUP_NAME
from src.features.packages.schemas import PackageConfigDTO, PackageDTO, PackageMapping
from src.shared.schemas import TreeNode
from src.shared.utils import unpack_group_key


def assign_default_group(item: PackageDTO) -> PackageDTO:
    if item.group_id is None or item.group_name is None:
        item.group_id = DEFAULT_GROUP_ID
        item.group_name = DEFAULT_GROUP_NAME
    return item


def create_tree_node_from_package_dto(data: PackageDTO) -> TreeNode:
    """
    Creates a TreeNode from a UserFormsSummary object.

    Args:
        data (UserFormsSummary): Object containing form or group data.

    Returns:
        TreeNode: A tree node representing the form or group.
    """
    return TreeNode(
        key=str(data.bulk_id),
        title=data.short_name,  # Usar el nombre corto como etiqueta
        data=data,  # Asociar los datos del formulario
        children=None,  # No tiene hijos inicialmente
        icon="fa-solid fa-clipboard-list",
        is_leaf=True
    )


def build_tree_from_grouped_items(group_id: str | int | None, group_name: str | None,
                                  items: list[PackageDTO]) -> TreeNode:
    """
    Builds a parent node with its children from a list of grouped items.

    Args:
        group_id (Optional[int]): ID of the group (can be None if there's no group).
        group_name (Optional[str]): Name of the group (can be None if there's no group).
        items (list[PackageDTO]): List of items belonging to the group.

    Returns:
        TreeNode: Parent node representing the group, with its associated children.
    """
    children = [create_tree_node_from_package_dto(item) for item in items]  # Crear nodos hijos
    return TreeNode(
        key=str(group_id),
        title=group_name or "No Group",
        data=None,
        children=children,
        icon="fa-solid fa-folder",
        expanded_icon="fa-solid fa-folder-open",
        collapsed_icon="fa-solid fa-folder-closed",
        expanded=True,
        is_leaf=False
    )

def map_packages_to_tree(collection: list[PackageDTO], use_default_group: bool = True) -> list[TreeNode]:
    """
    Maps a collection of summarized forms into a hierarchical tree structure.

    Args:
        collection (List[UserFormsSummary]): List of UserFormsSummary objects representing forms.

    Returns:
        List[TreeNode]: List of root nodes representing the hierarchical structure.
    """
    # Aplicar grupo por defecto si está habilitado
    if use_default_group:
        collection = [assign_default_group(item) for item in collection]

    # Ordenar la colección por group_id y group_name para asegurar que `groupby` funcione correctamente
    # collection.sort(key=lambda x: (x.group_id, x.group_name))

    # Agrupar los elementos por su clave de grupo
    grouped_iterators = groupby(collection, key=lambda x: (x.group_id, x.group_name))
    tree_nodes = []

    for group_key, group_items in grouped_iterators:
        # Desempaquetar la clave de grupo
        group_id, group_name = unpack_group_key(group_key)
        items = list(group_items)  # Convertir el iterador a una lista

        # Crear nodos según si hay grupo o no
        if group_id is None:
            # Sin grupo: cada elemento se convierte en un nodo raíz
            tree_nodes.extend(create_tree_node_from_package_dto(item) for item in items)
        else:
            # Con grupo: crear un nodo padre y agregar los elementos como hijos
            group_node = build_tree_from_grouped_items(group_id, group_name, items)
            tree_nodes.append(group_node)

    return tree_nodes


def map_package_config_to_mapping(package_config: PackageConfigDTO, next_period: dict) -> PackageMapping:
    return PackageMapping(
        bulk_id=package_config.bulk_id,
        bulk_code=package_config.bulk_code,
        form_id=package_config.form_id,
        form_code=package_config.form_code,
        form_name=package_config.short_name,
        sheet_name=package_config.import_query.sheet_name if package_config.import_query else None,
        range=package_config.import_query.use_columns if package_config.import_query else None,
        period_id=package_config.period_id,
        period_code=package_config.period_code,
        last_period=package_config.period_label,
        next_period=next_period['periodLabel'],
    )
