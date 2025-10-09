#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import (
    TYPE_CHECKING,
)

import numpy as np
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.basesections import (
    ElementalComposition,
    Entity,
)
from nomad.datamodel.metainfo.eln import Chemical, Instrument
from nomad.datamodel.metainfo.workflow import Link
from nomad.metainfo import (
    Datetime,
    MEnum,
    Package,
    Quantity,
    Section,
    SubSection,
)
from schema_packages.Items import Item, ItemsPermitted
from schema_packages.utils import parse_chemical_formula

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

m_package = Package(name='General organization and equipment for fabrication')


class TechniqueSubCategory(ArchiveSection):
    m_def = Section(
        a_eln={'properties': {'order': ['name', 'id', 'description']}},
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class TechniqueMainCategory(ArchiveSection):
    m_def = Section(
        a_eln={'properties': {'order': ['name', 'id', 'description']}},
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )
    technique_sub_categories = SubSection(
        section_def=TechniqueSubCategory,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class TechniqueGeneralCategory(ArchiveSection):
    m_def = Section()
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )
    technique_main_categories = SubSection(
        section_def=TechniqueMainCategory,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class TechniqueCategories(EntryData, ArchiveSection):
    m_def = Section(
        a_eln={'properties': {'order': ['name', 'description']}},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    technique_general_categories = SubSection(
        section_def=TechniqueGeneralCategory,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class EquipmentTechnique(ArchiveSection):
    m_def = Section(
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'id',
                    'description',
                    'techniqueGeneralCategory',
                    'techniqueMainCategory',
                    'techniqueSubCategory',
                    'genericEquipmentName',
                    'referencingcategorization',
                ]
            }
        },
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )
    genericEquipmentName = Quantity(
        type=str,
        description='Generic equipment that does the activity, f.e. etcher for etching',
        a_eln={'component': 'StringEditQuantity'},
    )
    techniqueGeneralCategory = Quantity(
        type=MEnum(
            'Add',
            'Characterize',
            'Remove',
            'Transform',
        ),
        a_eln={'component': 'EnumEditQuantity'},
    )
    techniqueMainCategory = Quantity(
        type=MEnum(
            [
                'synthesis',
                'integration',
                'doping',
                'dicing',
                'thermal processing',
                'lithography',
                'etching',
                'mechanical testing methods',
                'microscopy based methods',
                'spectroscopy based methods',
                'diffraction based methods',
                'light scattering techniques for nanoparticle analysis',
                'tribological characterisation',
                'thermal analysis methods',
                'electrical characterisation methods',
                'magnetic characterisation methods',
            ]
        ),
        a_eln={'component': 'AutocompleteEditQuantity'},
    )
    techniqueSubCategory = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    referencingcategorization = Quantity(
        type=TechniqueSubCategory,
        description='Reference to the taxonomy adopted',
        a_eln={'component': 'ReferenceEditQuantity'},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class FabricationProductType(ArchiveSection):
    m_def = Section(
        a_eln={'properties': {'order': ['name', 'description', 'id']}},
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class ListofProductType(EntryData, ArchiveSection):
    m_def = Section()

    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )
    available_products = SubSection(
        section_def=FabricationProductType,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class FabricationProcessStepBase(ArchiveSection):
    m_def = Section(
        definition="""
        Atomistic component of a generic fabrication step, it should be inherited
        """,
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'tag',
                    'starting_date',
                    'ending_date',
                    'duration',
                    'notes',
                ],
            },
        },
    )
    name = Quantity(
        type=str,
        description='Title assigned to the step',
        a_eln={'component': 'StringEditQuantity'},
    )
    tag = Quantity(
        type=str,
        description='Role of the step in fabrication (effective, conditioning, etc.)',
        a_eln={'component': 'StringEditQuantity'},
    )
    starting_date = Quantity(
        type=Datetime,
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    ending_date = Quantity(
        type=Datetime,
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    duration = Quantity(
        type=np.float64,
        description='Time used in this single atomic step',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'minute'},
        unit='minute',
    )
    notes = Quantity(
        type=str,
        description='Field to save annotations useful for the step.',
        a_eln={'component': 'RichTextEditQuantity'},
    )


class Jobdone(ArchiveSection):
    m_def = Section(
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'job_number',
                    'notes',
                    'starting_date',
                    'ending_date',
                    'id_item_processed',
                    'referenced_activity',
                ]
            }
        },
    )
    name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    job_number = Quantity(
        type=int,
        a_eln={'component': 'NumberEditQuantity'},
    )
    notes = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    starting_date = Quantity(
        type=Datetime,
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    ending_date = Quantity(
        type=Datetime,
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    id_items_processed = Quantity(
        type=int,
        a_eln={'component': 'NumberEditQuantity'},
        shape=['*'],
    )
    referenced_activities = Quantity(
        type=FabricationProcessStepBase,
        shape=['*'],
        a_eln={'component': 'ReferenceEditQuantity'},
    )


class Equipment(Instrument, EntryData, ArchiveSection):
    m_def = Section(
        description="""
        Base class to inherit to describe various kind of fabrication equipment
        """,
        a_eln={
            'hide': [
                'datetime',
            ],
            'properties': {
                'order': [
                    'name',
                    'lab_id',
                    'description',
                    'affiliation',
                    'institution',
                    'product_model',
                    'manufacturer_name',
                    'inventary_code',
                    'is_bookable',
                    'automatic_loading',
                    'contamination_class',
                    'notes',
                ],
            },
        },
    )
    lab_id = Quantity(
        type=str,
        description='ID assigned by lab for findability',
        a_eln={'component': 'StringEditQuantity', 'label': 'id'},
    )
    inventary_code = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    affiliation = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    institution = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    manufacturer_name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    product_model = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    automatic_loading = Quantity(
        type=bool,
        a_eln={'component': 'BoolEditQuantity'},
    )
    is_bookable = Quantity(
        type=bool,
        a_eln={'component': 'BoolEditQuantity'},
    )
    contamination_class = Quantity(
        type=int,
        description='Level of quality of the environment in the equipment',
        a_eln={'component': 'NumberEditQuantity'},
    )

    notes = Quantity(
        type=str,
        a_eln={
            'component': 'RichTextEditQuantity',
        },
    )

    equipmentTechniques = SubSection(
        section_def=EquipmentTechnique,
        repeats=True,
    )
    permittedItems = SubSection(
        section_def=ItemsPermitted,
        repeats=True,
    )
    equipmentLogBook = SubSection(
        section_def=Jobdone,
        repeats=True,
    )


class EquipmentReference(Link, ArchiveSection):
    m_def = Section()

    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )

    notes = Quantity(
        type=str,
        a_eln={'component': 'RichTextEditQuantity'},
    )

    section = Quantity(
        type=Equipment,
        a_eln={'component': 'ReferenceEditQuantity'},
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if self.section is not None:
            super().normalize(archive, logger)
            try:
                self.name = self.section.name
                self.id = self.section.lab_id
            except Exception as e:
                raise e


class User(ArchiveSection):
    m_def = Section(description='Section to describe who performed a step')

    name = Quantity(
        type=str,
        description='Name of one of the user involved',
        a_eln={'component': 'StringEditQuantity'},
    )

    role = Quantity(
        type=str,
        description='Role of the user in the lab or for the experiment',
        a_eln={'component': 'StringEditQuantity'},
    )

    affiliation = Quantity(
        type=str,
        description='Affiliation of the user',
        a_eln={'component': 'StringEditQuantity'},
    )

    address = Quantity(
        type=str,
        description='Address of the office for the user',
        a_eln={'component': 'StringEditQuantity'},
    )

    telephone_number = Quantity(
        type=str,
        description='Telephone number to contact the user',
        a_eln={'component': 'StringEditQuantity'},
    )

    fax_number = Quantity(
        type=str,
        description='Fax number to contact the user',
        a_eln={'component': 'StringEditQuantity'},
    )

    email = Quantity(
        type=str,
        description='Email address to contact the user',
        a_eln={'component': 'StringEditQuantity'},
    )

    ORCID = Quantity(
        type=str,
        description="""
            an author code, Open Researcher and Contributor ID, defined by
            https://orcid.org and expressed as a URI
        """,
        a_eln={'component': 'StringEditQuantity'},
    )

    facility_user_id = Quantity(
        type=str,
        description="""
            facility based unique identifier for this person e.g. the identification
            code on the facility address/contact database
        """,
        a_eln={'component': 'StringEditQuantity'},
    )


class FabricationProcessStep(FabricationProcessStepBase, EntryData):
    m_def = Section(
        description="""
        With fabrication process step is intended an action upon an item to modify its
        native shape or in general property. Steps are specilized in specific techinques
        sub category and technology instances. Combined they form a process.
        """,
        a_eln={
            'hide': ['tag', 'duration'],
            'properties': {
                'order': [
                    'name',
                    'step_id',
                    'description',
                    'affiliation',
                    'location',
                    'institution',
                    'facility',
                    'laboratory',
                    'id_item_processed',
                    'starting_date',
                    'ending_date',
                    'step_type',
                    'definition_of_process_step',
                    'keywords',
                    'recipe_name',
                    'recipe_file',
                    'recipe_preview',
                    'notes',
                ],
            },
        },
    )

    id_item_processed = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    step_id = Quantity(
        type=str,
        description="""
            Unique identifier for the experiment, defined by the facility, possibly
            linked to the proposals.
        """,
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        description='Brief summary of the experiment, including key objectives',
        a_eln={'component': 'RichTextEditQuantity'},
    )
    affiliation = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    location = Quantity(
        type=str,
        description='City and country where the experiment took place',
        a_eln={'component': 'StringEditQuantity'},
    )
    institution = Quantity(
        type=str,
        description='Name of the institution hosting the facility',
        a_eln={'component': 'StringEditQuantity'},
    )
    facility = Quantity(
        type=str,
        description='Name of the experimental facility',
        a_eln={'component': 'StringEditQuantity'},
    )
    laboratory = Quantity(
        type=str,
        description='Name of the laboratory or beamline',
        a_eln={'component': 'StringEditQuantity'},
    )
    step_type = Quantity(
        type=str,
        description="""
        More specific definition of the step type performed for example SEM for
        electron microscopy
        """,
        a_eln={'component': 'StringEditQuantity'},
    )
    definition_of_process_step = Quantity(
        type=TechniqueSubCategory,
        description='Reference to the particular technique type used',
        a_eln={'component': 'ReferenceEditQuantity'},
    )
    keywords = Quantity(
        type=str,
        description='Some additional words describing the step',
        a_eln={'component': 'StringEditQuantity'},
    )
    recipe_name = Quantity(
        type=str,
        description='Field containing the name of the recipe used',
        a_eln={'component': 'StringEditQuantity'},
    )
    recipe_file = Quantity(
        type=str,
        description='If filled it should contain the file of the recipe for download',
        a_eln={'component': 'FileEditQuantity'},
    )
    recipe_preview = Quantity(
        type=str,
        description='This field could be used to give a preview of the recipe file',
        a_eln={'component': 'RichTextEditQuantity'},
    )

    instrument = SubSection(
        section_def=EquipmentReference,
        description='Reference to the equipments used during the step',
        repeats=False,
    )

    users = SubSection(
        section_def=User, description='List of users involved in the step', repeats=True
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class FabricationOutput(ArchiveSection):
    m_def = Section(
        description="""
        Ideal class to inherit to define any kind of outputs from a FabricationProcess.
        """
    )


class FabricationProcess(EntryData, ArchiveSection):
    m_def = Section(
        description="""
        For fabrication process is intended a series of steps within which an item is
        modified to generate some features useful for future applications. Processes
        have outputs consisting in particular product type, e.g. wave guides, or also 
        row materials. To describe fabrication of materials you should use the class
        MaterialProductionProcess. 
        """,
        a_eln={
            'properties': {
                'order': [
                    'name',
                    'project',
                    'affiliation',
                    'id_proposal',
                    'id_item_processed',
                    'location',
                    'cost_model',
                    'description',
                    'author',
                    'starting_date',
                    'ending_date',
                    'generic_product_name',
                    'fabricationProductType',
                    'notes',
                ]
            }
        },
    )
    id_proposal = Quantity(
        type=str,
        description='Unique identifier associated to the process',
        a_eln={'component': 'StringEditQuantity'},
    )
    id_item_processed = Quantity(
        type=str,
        description='Unique identifier associated to the item undergoing the process',
        a_eln={'component': 'StringEditQuantity'},
    )
    project = Quantity(
        type=str,
        description='Fill this field if the process is performed in a project',
        a_eln={'component': 'StringEditQuantity'},
    )
    affiliation = Quantity(
        type=str,
        description="""
        Field to describe an eventual association within which the process is performed
        """,
        a_eln={'component': 'StringEditQuantity'},
    )
    location = Quantity(
        type=str,
        description='Where the process is performed',
        a_eln={'component': 'StringEditQuantity'},
    )
    name = Quantity(
        type=str,
        description='Denomination for the process',
        a_eln={'component': 'StringEditQuantity'},
    )
    description = Quantity(
        type=str,
        description='Field to describe the process briefly',
        a_eln={'component': 'RichTextEditQuantity'},
    )
    author = Quantity(
        type=str,
        description='Intended as who created the process',
        a_eln={'component': 'StringEditQuantity'},
    )
    cost_model = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    starting_date = Quantity(
        type=Datetime,
        description='When the process is effectively started',
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    ending_date = Quantity(
        type=Datetime,
        description='When the process is effectively finished',
        a_eln={'component': 'DateTimeEditQuantity'},
    )
    notes = Quantity(
        type=str,
        description='Additional field to save additional information',
        a_eln={'component': 'RichTextEditQuantity'},
    )
    generic_product_name = Quantity(
        type=str,
        description='Intended as what kind of product for the process is expected',
        a_eln={'component': 'StringEditQuantity'},
    )
    fabricationProductType = Quantity(
        type=ListofProductType,
        description="""
        Link to a NOMAD instance (if exist) describing the product expected
        """,
        a_eln={'component': 'ReferenceEditQuantity'},
    )
    steps = Quantity(
        type=FabricationProcessStep,
        shape=['*'],
        description="""
        An array with the references to the entries where the step is described more
        extensively
        """,
        a_eln={'component': 'ReferenceEditQuantity'},
    )

    output = SubSection(
        section_def=FabricationOutput,
        description='Subsection to save some results of the output obtained.',
        repeat=False,
    )


class StartingMaterial(Chemical, FabricationProcessStep, ArchiveSection):
    m_def = Section(
        a_eln={
            'hide': [
                'description',
                'lab_id',
                'datetime',
                'comment',
                'duration',
                'end_time',
                'start_time',
                'recipe_name',
            ],
            'properties': {
                'order': [
                    'job_number',
                    'name',
                    'description',
                    'location',
                    'operator',
                    'room',
                    'id_item_processed',
                    'starting_date',
                    'ending_date',
                    'step_type',
                    'definition_of_process_step',
                    'short_name',
                    'chemical_formula',
                    'manufacturer_name',
                    'wafer_quantity',
                    'wafer_resistivity',
                    'wafer_orientation',
                    'wafer_thickness',
                    'wafer_surface_finish',
                    'wafer_diameter',
                    'wafer_doping',
                    'notes',
                ]
            },
        },
    )
    short_name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity', 'label': 'wafer material'},
    )
    manufacturer_name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    wafer_quantity = Quantity(
        type=int,
        a_eln={'component': 'NumberEditQuantity'},
    )
    wafer_resistivity = Quantity(
        type=np.float64,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'ohm*cm'},
        unit='ohm*cm',
    )
    wafer_thickness = Quantity(
        type=np.float64,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'um'},
        unit='um',
    )
    wafer_orientation = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    wafer_surface_finish = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    wafer_diameter = Quantity(
        type=np.float64,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'mm'},
        unit='mm',
    )
    wafer_doping = Quantity(
        type=MEnum(
            'p',
            'n',
            'no',
        ),
        a_eln={'component': 'EnumEditQuantity'},
    )

    elemental_composition = SubSection(section_def=ElementalComposition, repeats=True)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        if self.chemical_formula:
            elements, counts = parse_chemical_formula(self.chemical_formula)
            total = 0
            for token in counts:
                total += int(token)
            if total != 0:
                elemental_fraction = np.array(counts) / total
                elementality = []
                i = 0
                for entry in elements:
                    elemental_try = ElementalComposition()
                    elemental_try.element = entry
                    elemental_try.atomic_fraction = elemental_fraction[i]
                    i += 1
                    elementality.append(elemental_try)
            else:
                print('No elements provided')
            self.elemental_composition = elementality


class ItemParenting(Entity, EntryData, ArchiveSection):
    m_def = Section(
        a_eln={
            'hide': ['lab_id'],
            'properties': {
                'order': [
                    'name',
                    'datetime',
                    'id',
                ],
            },
        }
    )
    id = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    inputs = SubSection(
        section_def=StartingMaterial,
        repeats=True,
    )
    parenting_steps = SubSection(section_def=FabricationProcessStep, repeats=True)
    outputs = SubSection(
        section_def=Item,
        repeats=True,
    )


class ItemParentingLink(Link, ArchiveSection):
    m_def = Section()

    Section = Quantity(
        type=ItemParenting,
        a_eln={'component': 'ReferenceEditQuantity'},
    )


class ObservationMeasurements(FabricationProcessStep, ArchiveSection):
    m_def = Section(
        a_eln={
            'hide': [
                'description',
                'lab_id',
                'datetime',
                'comment',
                'duration',
                'end_time',
                'start_time',
                'recipe_name',
            ],
            'properties': {
                'order': [
                    'job_number',
                    'name',
                    'description',
                    'location',
                    'operator',
                    'room',
                    'id_item_processed',
                    'starting_date',
                    'ending_date',
                    'step_type',
                    'definition_of_process_step',
                    'activity_type',
                    'short_name',
                    'duration_target',
                    'image_name',
                    'thickness_measurements',
                    'electrical_measurements',
                    'notes',
                ]
            },
        },
    )
    short_name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity', 'label': 'Equipment used'},
    )
    activity_type = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    duration_target = Quantity(
        type=np.float64,
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'minute'},
        unit='minute',
    )
    image_name = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    thickness_measurements = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )
    electrical_measurements = Quantity(
        type=str,
        a_eln={'component': 'StringEditQuantity'},
    )


m_package.__init_metainfo__()
