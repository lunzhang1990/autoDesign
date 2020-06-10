import DSGRN
import itertools
import time
import sys

def is_ipsc_fixed_point(morse_node, morse_graph):
    isFP = lambda morse_node : morse_graph.annotation(morse_node)[0].startswith('FP')
    isStable = lambda morse_node : len(morse_graph.poset().children(morse_node)) == 0
    isStableFP = lambda morse_node : isFP(morse_node) and isStable(morse_node)

    if isStableFP(morse_node):
        annotation = morse_graph.annotation(morse_node)[0]
        digits = [int(s) for s in annotation.replace(",", "").split() if s.isdigit()]
        if digits == [0, 0, 0, 0, 0]:
            return True
    return False

def is_day8_fixed_point(morse_node, morse_graph):
    isFP = lambda morse_node : morse_graph.annotation(morse_node)[0].startswith('FP')
    isStable = lambda morse_node : len(morse_graph.poset().children(morse_node)) == 0
    isStableFP = lambda morse_node : isFP(morse_node) and isStable(morse_node)

    if isStableFP(morse_node):
        annotation = morse_graph.annotation(morse_node)[0]
        digits = [int(s) for s in annotation.replace(",", "").split() if s.isdigit()]
        # High [2, 1, 2, 1, 2]
        if digits == [2, 1, 2, 0, 2]:
            return True
    return False

def NetworkSpecStr(net_spec):
    net_spec_str = ""

    spec = "SOX17 : "
    activators = ' + '.join([ 'Y' + str(j) for j in range(0,2) if net_spec[j] == 1])
    repressors = ')('.join([ '~Y' + str(j) for j in range(0,2) if net_spec[j] == -1])
    if activators:
        activators = '(' + activators + ')'
    if repressors:
        repressors = '(' + repressors + ')'
    spec += activators + repressors + "\n "
    spec = spec.replace("Y0", "TAFP2C")
    spec = spec.replace("Y1", "ID1")
    net_spec_str += spec

    spec = "TAFP2C : "
    activators = ' + '.join([ 'Y' + str(j) for j in range(2,5) if net_spec[j] == 1])
    repressors = ')('.join([ '~Y' + str(j) for j in range(2,5) if net_spec[j] == -1])
    if activators:
        activators = '(' + activators + ')'
    if repressors:
        repressors = '(' + repressors + ')'
    spec += activators + repressors + "\n "
    spec = spec.replace("Y2", "HAND1")
    spec = spec.replace("Y3", "ID1")
    spec = spec.replace("Y4", "SOX17")
    net_spec_str += spec

    spec = "PRDMI : " + ("~SOX17" if net_spec[5] == -1 else "SOX17") + "\n "
    net_spec_str += spec

    spec = "HAND1 : " + ("~PRDMI" if net_spec[6] == -1 else "PRDMI") + "\n "
    net_spec_str += spec

    spec = "ID1 : " + ("~PRDMI" if net_spec[7] == -1 else "PRDMI")
    net_spec_str += spec

    return net_spec_str

def compute_query(network_specs, spec_index):
    start_time = time.time()

    net_spec = network_specs[spec_index]
    net_spec_str = NetworkSpecStr(net_spec)
    network = DSGRN.Network(net_spec_str)
    parameter_graph = DSGRN.ParameterGraph(network)

    ipsc_parameters = []
    day8_parameters = []
    both_parameters = []

    for parameter_index in range(0, parameter_graph.size()):
        parameter = parameter_graph.parameter(parameter_index)
        domain_graph = DSGRN.DomainGraph(parameter)
        morse_decomposition = DSGRN.MorseDecomposition(domain_graph.digraph())
        morse_graph = DSGRN.MorseGraph(domain_graph, morse_decomposition)
        morse_nodes = range(0, morse_graph.poset().size())
        has_ipsc_FP = any(is_ipsc_fixed_point(node, morse_graph) for node in morse_nodes)
        has_day8_FP = any(is_day8_fixed_point(node, morse_graph) for node in morse_nodes)
        if has_ipsc_FP:
            ipsc_parameters.append(parameter_index)
        if has_day8_FP:
            day8_parameters.append(parameter_index)
        if has_ipsc_FP and has_day8_FP:
            both_parameters.append(parameter_index)

    num_pars = parameter_graph.size()
    num_ipsc_pars = len(ipsc_parameters)
    num_day8_pars = len(day8_parameters)
    num_both_pars = len(both_parameters)

    end_time = time.time()
    tot_time = end_time - start_time

    net_spec_fname = 'net_spec_' + str(spec_index) + '.txt'
    with open(net_spec_fname, 'w') as outfile:
        outfile.write(' '.join(str(k) for k in net_spec) + '\n')

    results = (num_pars, num_ipsc_pars, num_day8_pars, num_both_pars, tot_time)
    results_fname = 'results_' + str(spec_index) + '.txt'
    with open(results_fname, 'w') as outfile:
        outfile.write(' '.join(str(x) for x in results) + '\n')

    # return num_pars, num_ipsc_pars, num_day8_pars, num_both_pars, tot_time

if __name__ == "__main__":
    # Read command line argument
    if len(sys.argv) < 2:
        print("./ComputeQuery index")
        exit(1)

    spec_index = int(sys.argv[1])

    # Compute the cartesian product [-1, 1]^8
    vals = [-1, 1]
    list_vals = [vals, vals, vals, vals, vals, vals, vals, vals]
    network_specs = [ element for element in itertools.product(*list_vals) ]

    # Compute with network spec_index among the 256 networks
    compute_query(network_specs, spec_index)

    exit(0)
