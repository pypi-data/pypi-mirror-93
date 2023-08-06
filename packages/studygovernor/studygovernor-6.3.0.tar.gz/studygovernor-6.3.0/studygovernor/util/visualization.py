import os
import subprocess
import yaml
from datetime import datetime

from studygovernor import models


STYLE_MAP = {
    'external_program': 'fillcolor=darkolivegreen1',
    'send_mail': 'fillcolor=darkgreen,fontcolor=white',
    'pidb': 'fillcolor=lightsalmon',
    'fastr': 'fillcolor=lightskyblue1',
    'create_task': 'fillcolor=lightgoldenrod1',
    'done': 'fillcolor=indigo,fontcolor=white,color=darkolivegreen1,penwidth=3.0',
    'untracked': 'fillcolor=indigo,fontcolor=white,color=plum1,penwidth=3.0',
    'unspecified': 'fillcolor=plum1',
    'failed': 'color=red,penwidth=3.0'
}


def _visualize(workflow_label, states, transitions):
    """ Visualize the states and transitions in a graph. """

    # Setup the visualization.
    lines = ['digraph graphname { node [shape=box,style=filled,fillcolor=white,margin="0.45,0.055"]; ']

    # Create a legend
    lines.append('subgraph cluster_legend { color=black label=Legend ')
    for function, style in STYLE_MAP.items():
        lines.append(' "{function} node" [label="{function} node",{style},]; '.format(function=function, style=style))
    for x, y in zip(STYLE_MAP.keys(), list(STYLE_MAP.keys())[1:]):
        lines.append(' "{} node" -> "{} node" [color=invis];'.format(x, y))
    lines.append("}")

    # Generate the state nodes.
    for idx, s in states:
        extra_attrs = ""
        if s['callback'] is not None:
            extra_attrs += "{style},".format(style=STYLE_MAP.get(s['callback']['function'], STYLE_MAP['unspecified']))
        if 'failed' in s['label']:
            extra_attrs += STYLE_MAP['failed']
        if s['label'] in list(STYLE_MAP.keys()):
            extra_attrs += "{},".format(STYLE_MAP[s['label']])
        lines.append('  "{label}" [label="{id}: {label}",{extra}];'.format(id=idx, label=s['label'], extra=extra_attrs))

    # Generate transitions.
    for idx, t in transitions:
        lines.append('  "{}" -> "{}" [label="{}"];'.format(t["source"], t["destination"], idx))

    # Close the digraph
    lines.append(f'labelloc="t";\nlabel="Workflow: {workflow_label}  generated on: {datetime.now().isoformat()}";')
    lines.append('}')

    return workflow_label, lines


def visualize_from_db():
    """ Visualize all workflows in the study governor. """
    visualizations = []
    for workflow in models.Workflow.query.all():
        state_objects = models.State.query.filter_by(workflow=workflow).all()
        states = [
            (
                so.id,
                {
                    "label": so.label,
                    "callback": yaml.load(so.callback, Loader=yaml.SafeLoader) if so.callback is not None else None
                }
            )
            for so in state_objects
        ]

        transition_objects = (
            models.Transition.query.join(
                models.State, models.Transition.source_state_id == models.State.id
            )
            .filter(models.State.workflow == workflow)
            .all()
        )
        transitions = [
            (
                t.id,
                {
                    "source": t.source_state.label,
                    "destination": t.destination_state.label,
                },
            )
            for t in transition_objects
        ]

        visualizations.append(_visualize(workflow.label, states, transitions))

    return visualizations


def visualize_from_config(filename):
    try:
        with open(filename) as fh:
            workflow_definition = yaml.safe_load(fh)
    except IOError as e:
        print("IOError: {}".format(e))
        print("Please specify a valid JSON or YAML file.")
        return

    workflow = workflow_definition['label']
    states = [(idx+1, s) for idx, s in enumerate(workflow_definition['states'])]
    transitions = [(idx+1, t) for idx, t in enumerate(workflow_definition['transitions'])]

    return _visualize(workflow, states, transitions)


def write_visualization_to_file(visualization, fmt):
    workflow = visualization[0]
    dot_spec = visualization[1]

    dot_file = f"{workflow}.dot"
    output_file = f"{workflow}.{fmt}"

    print(f"Writing {workflow} to {output_file}")
    with open(dot_file, 'w') as df:
        for line in dot_spec:
            df.write(line)
            df.write('\n')

    try:
        proc = subprocess.Popen(['dot', f'-T{fmt}', f'-o{output_file}', dot_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        if stderr is not None:
            print('Subprocess call to do finished with stdout: {}, stderr: {}'.format(stdout, stderr))

        if not os.path.exists(output_file):
            print('Network draw failed the graphviz coversion:\n{}'.format(stdout))
    except OSError:
        print("Cannot convert %s to an svg image. Please put dot (from GraphViz) in your PATH.", output_file)
        return None
    finally:
        if os.path.isfile(dot_file):
            os.remove(dot_file)
