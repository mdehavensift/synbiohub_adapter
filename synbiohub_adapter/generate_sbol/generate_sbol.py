import argparse
import csv
import sys
import os
from pySBOLx.pySBOLx import XDocument

SD2_DESIGN_NS = 'http://hub.sd2e.org/user/sd2e/design'
CHEBI_NS = 'http://identifiers.org/chebi/'

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', default=[f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')])
    parser.add_argument('-o', '--output', nargs='?', default='generated_sbol.xml')
    parser.add_argument('-m', '--om', nargs='?', default='om-2.0.rdf')
    args = parser.parse_args(args)

    doc = generate_sbol(args.input, args.om)
    
    doc.write(args.output)

def generate_sbol(csv_files, om_file):
    doc = XDocument()
    doc.configure_namespace(SD2_DESIGN_NS)
    doc.configure_options(False, False)

    try:
        om = doc.read_om(om_file)
    except:
        om = None

    generate_device_switcher = {
        'Bead': generate_bead,
        'CHEBI': generate_chebi,
        'DNA': generate_dna,
        'Enzyme': generate_enzyme,
        'Fluorescent_Bead': generate_fluorescent_bead,
        'Plasmid': generate_plasmid,
        'Protein': generate_protein,
        'RNA': generate_rna,
        'Strain': generate_strain
    }

    generate_system_switcher = {
        'Buffer': generate_buffer,
        'Control': generate_control,
        'Gate': generate_gate, 
        'Media': generate_media,
        'Solution': generate_solution
    }

    generate_input_switcher = {
        'Inducer': generate_inducer
    }
    
    for csv_file in csv_files:
        generate_sbol_helper(doc, csv_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om)

    return doc

def generate_sbol_helper(doc, csv_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om=None, out_devices=[], out_systems=[], out_inputs=[], out_measures={}):
    with open(csv_file) as csv_content:
        csv_reader = csv.reader(csv_content)
        header = {k: v for v, k in enumerate(next(csv_reader))}

        for row in csv_reader:
            generate_type = row[header['Type']]

            try:
                generate_system = generate_system_switcher[generate_type]

                devices = []
                systems = []
                inputs = []
                measures = {}

                try:
                    aux_file = os.path.join(os.path.dirname(csv_file), row[header['Composition_File']])

                    generate_sbol_helper(doc, aux_file, generate_device_switcher, generate_system_switcher, generate_input_switcher, om, devices, systems, inputs, measures)
                except:
                    pass

                identified = generate_system(doc, row, header, devices, systems, inputs, measures)

                out_systems.append(identified)
            except:
                try:
                    generate_device = generate_device_switcher[generate_type]

                    identified = generate_device(doc, row, header)

                    out_devices.append(identified)
                except:
                    generate_input = generate_input_switcher[generate_type]

                    identified = generate_input(doc, row, header)

                    out_inputs.append(identified)

            try:
                out_measures[identified.displayId] = generate_concentration(doc, row, header, om)
            except:
                try:
                    out_measures[identified.displayId] = generate_volume(doc, row, header, om)
                except:
                    pass

def generate_volume(doc, row, header, om):
    try:
        unit = generate_volume_unit(doc, row, header, om)

        return {'mag': float(row[header['Volume']]), 'unit': unit, 'id': 'volume'}
    except:
        return {'mag': float(row[header['Volume']]), 'id': 'volume'}

def generate_concentration(doc, row, header, om):
    try:
        unit = generate_concentration_unit(doc, row, header, om)

        return {'mag': float(row[header['Concentration']]), 'unit': unit, 'id': 'concentration'}
    except:
        return {'mag': float(row[header['Concentration']]), 'id': 'concentration'}

def generate_buffer(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('buffer ' + display_id)

    return doc.create_buffer(devices, systems, inputs, measures, display_id, name, descr)

def generate_control(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('control ' + display_id)

    return doc.create_control(devices, systems, inputs, measures, display_id, name, descr)

def generate_gate(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('gate ' + display_id)

    return doc.create_gate(devices, systems, inputs, measures, display_id, name, descr)

def generate_media(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('media ' + display_id)

    return doc.create_media(devices, systems, inputs, measures, display_id, name, descr)

def generate_solution(doc, row, header, devices=[], systems=[], inputs=[], measures={}):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('solution ' + display_id)

    return doc.create_solution(devices, systems, inputs, measures, display_id, name, descr)

def generate_bead(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('bead ' + display_id)

    return doc.create_bead(display_id, name, descr)

def generate_chebi(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('chebi ' + display_id)

    return doc.create_component_definition(display_id, name, descr, CHEBI_NS + row[header['CHEBI']])

def generate_dna(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('dna ' + display_id)

    return doc.create_dna(display_id, name, descr)

def generate_enzyme(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('enzyme ' + display_id)

    return doc.create_enzyme(display_id, name, descr)

def generate_fluorescent_bead(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('fluorescent_bead ' + display_id)

    return doc.create_fluorescent_bead(display_id, name, descr)

def generate_plasmid(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('plasmid ' + display_id)

    return doc.create_plasmid(display_id, name, descr)

def generate_protein(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('protein ' + display_id)

    return doc.create_protein(display_id, name, descr)

def generate_rna(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('rna ' + display_id)

    return doc.create_rna(display_id, name, descr)

def generate_strain(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('strain ' + display_id)

    return doc.create_strain(display_id, name, descr)

def generate_inducer(doc, row, header):
    display_id = row[header['ID']]
    try:
        name = row[header['Name']]
    except:
        name = None
    try:
        descr = row[header['Description']]
    except:
        descr = None

    print('inducer ' + display_id)

    return doc.create_inducer(display_id, name, descr)

def generate_concentration_unit(doc, row, header, om):
    symbol = row[header['Concentration_Units']]

    assert len(symbol) > 0

    try:
        return doc.create_unit(om, symbol)
    except:
        return doc.create_unit(om=om, name=symbol)

def generate_volume_unit(doc, row, header, om):
    symbol = row[header['Volume_Units']]

    assert len(symbol) > 0

    try:
        return doc.create_unit(om, symbol)
    except:
        return doc.create_unit(om=om, name=symbol)

if __name__ == '__main__':
    main()