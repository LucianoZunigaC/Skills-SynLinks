from itertools import groupby
from typing import Sequence, List, Optional

from src.shared.schemas import ListItem, TreeNode
from .schemas import FormPeriodBase, FormEntry, CreateFormData, FormData, UserFormsSummary
from ...shared.utils import is_valid_float, is_valid_int, unpack_group_key


def map_period_to_list_item(period: FormPeriodBase) -> ListItem:
    return ListItem(id=period.id, title=period.period_code)


def process_form_entry(form_entry: FormEntry,
                       entities: Sequence[FormData], ) -> List[CreateFormData]:
    """
    Process a single form entry and match it with related entities.

    Args:
        form_entry (FormEntry): Form entry to be processed.
        entities (Sequence[FormData]): List of entities to match against.

    Returns:
        List[CreateFormData]: List of processed CreateFormData objects.
    """
    matching_entities = _filter_matching_entities(
        entities,
        col_number=int(form_entry.col_def.field) if is_valid_int(form_entry.col_def.field) else -1,
        row_number=form_entry.row_def.row_id
    )

    create_form_data_list = []
    for entity in matching_entities:
        create_form_data = _process_matching_entity(form_entry, entity)
        if create_form_data:
            create_form_data_list.append(create_form_data)

    return create_form_data_list


def _process_matching_entity(form_entry: FormEntry,
                             entity: FormData) -> CreateFormData | None:
    """
    Process a single matching entity and update its fields based on form entry.

    Args:
        form_entry (FormEntry): The submitted form entry.
        entity (Entity): Matching entity to be updated.

    Returns:
        CreateFormData | None: Processed CreateFormData object or None if invalid.
    """
    create_form_data = CreateFormData(**entity.model_dump(by_alias=True))

    # TODO: Obtener usuario conectado
    create_form_data.user_id = 'jmfuent'

    if entity.data_type_code == "DEC":
        if form_entry.value and is_valid_float(form_entry.value):
            create_form_data.value_dec = float(form_entry.value)
        else:
            create_form_data.value_dec = None
        return create_form_data
    return None


def _filter_matching_entities(
        related_entities: Sequence[FormData],
        row_number: int | None = None,
        col_number: int | None = None
) -> List[FormData]:
    """
    Filter matching entities based on label and other optional attributes.

    Args:
        related_entities (Sequence[Entity]): List of entities to filter.
        row_number (int | None): Optional row number.
        col_number (int | None): Optional col number.

    Returns:
        List[Entity]: Filtered list of entities that match the criteria.
    """

    return [
        entity
        for entity in related_entities
        if entity.col_number == col_number and entity.row_number == row_number]


def create_tree_node_from_summary(data: UserFormsSummary) -> TreeNode:
    """
    Creates a TreeNode from a UserFormsSummary object.

    Args:
        data (UserFormsSummary): Object containing form or group data.

    Returns:
        TreeNode: A tree node representing the form or group.
    """
    return TreeNode(
        key=str(data.form_id),
        title=data.short_name,  # Usar el nombre corto como etiqueta
        data=data,  # Asociar los datos del formulario
        children=None,  # No tiene hijos inicialmente
        icon="fa-solid fa-clipboard-list",
        is_leaf=True
    )


def build_tree_from_grouped_items(group_id: Optional[int], group_name: Optional[str],
                                  items: List['UserFormsSummary']) -> TreeNode:
    """
    Builds a parent node with its children from a list of grouped items.

    Args:
        group_id (Optional[int]): ID of the group (can be None if there's no group).
        group_name (Optional[str]): Name of the group (can be None if there's no group).
        items (List[UserFormsSummary]): List of items belonging to the group.

    Returns:
        TreeNode: Parent node representing the group, with its associated children.
    """
    children = [create_tree_node_from_summary(item) for item in items]  # Crear nodos hijos
    return TreeNode(
        key= f'group_{group_id}',
        title=group_name or "No Group",
        data=None,
        children=children,
        icon="fa-solid fa-folder",
        expanded_icon="fa-solid fa-folder-open",
        collapsed_icon="fa-solid fa-folder-closed",
        is_leaf=False
    )


def map_forms_to_tree(collection: List[UserFormsSummary]) -> List[TreeNode]:
    """
    Maps a collection of summarized forms into a hierarchical tree structure.

    Args:
        collection (List[UserFormsSummary]): List of UserFormsSummary objects representing forms.

    Returns:
        List[TreeNode]: List of root nodes representing the hierarchical structure.
    """
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
            tree_nodes.extend(create_tree_node_from_summary(item) for item in items)
        else:
            # Con grupo: crear un nodo padre y agregar los elementos como hijos
            group_node = build_tree_from_grouped_items(group_id, group_name, items)
            tree_nodes.append(group_node)

    return tree_nodes
