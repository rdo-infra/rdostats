def count_bugs_by_component(report):
    counts = {}
    for bug in report.bugs(status=report.status_open):
        comp = bug['component']
        counts[comp] = counts.get(comp, 0) + 1
    return counts


def component_graph(report,
                    line_width=75,
                    max_comp_len=None):
    counts = count_bugs_by_component(report)

    max_comp_len = (max_comp_len or
                    max(len(comp) for comp in counts))
    max_count = max(counts[k] for k in counts)

    extra_len = 10
    graph_width = line_width - max_comp_len - extra_len
    graph = []

    for comp in sorted(counts, key=lambda x: x.lower()):
        count = counts[comp]
        if len(comp) > max_comp_len:
            comp_display = '%s...' % (comp[:max_comp_len-3])
        else:
            comp_display = comp

        l = int(graph_width * (counts[comp] / (max_count * 1.0)))

        graph.append('%*s [%3d] %-*s' % (
            max_comp_len,
            comp_display,
            count,
            graph_width,
            '+' * l))

    return '\n'.join(graph)
