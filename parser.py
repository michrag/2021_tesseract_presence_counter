#!/usr/bin/env python

from collections import defaultdict
import re
from difflib import SequenceMatcher
import pprint
import json
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.ticker as plticker


participants = {}
participant_presences_map = {}


def populate_participants():
    global participants
    global participant_presences_map

    participants["Alice"] = ["Alice", "Ali"]
    participants["Bob"] = ["Bob", "bob", "bo"]
    # to be filled as needed

    participant_presences_map = dict.fromkeys(participants.keys(), [])


def process(content):
    day_participants_map = {}
    current_day = ""
    for line in content:
        if "WhatsApp" in line:
            match = re.search(r'(\d+-\d+-\d+)', line)
            date = match.group(1)
            #print(date)
            current_day = date
            # we may have more than one picture in a given day
            if date not in day_participants_map:
                day_participants_map[current_day] = []
        else:
            day_participants_map[current_day].append(line)

    #pprint.pprint(day_participants_map)

    return day_participants_map


def process_map(day_participants_map):
    global participants
    global participant_presences_map
    actual_day_participants_map = defaultdict(set)
    participant_presences_map = defaultdict(set)
    for day in day_participants_map:
        #print(day)
        for string in day_participants_map[day]:
            #print(string)
            for participant in participants:
                for alias in participants[participant]:
                    #print(alias)
                    # minimum string length is 4, on a 4-word name we accept 1-letter error, so a 0.25 tolerance
                    if similar(string, alias) >= 0.75:
                        actual_day_participants_map[day].add(participant)
                        participant_presences_map[participant].add(day)

    #print(actual_day_participants_map)
    #pprint.pprint(actual_day_participants_map)

    return actual_day_participants_map


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def create_day_number_of_participants_map(actual_day_participants_map):
    day_number_of_participants_map = {}
    for day in actual_day_participants_map:
        day_number_of_participants_map[day] = len(actual_day_participants_map[day])
        #print(f'{day} = {len(actual_day_participants_map[day])}')

    return day_number_of_participants_map


def create_participant_number_of_presence_map():
    global participant_presences_map
    participant_number_of_presence_map = {}
    for participant in participant_presences_map:
        participant_number_of_presence_map[participant] = len(participant_presences_map[participant])
        #print(f'{participant} = {len(participant_presences_map[participant])}')

    return participant_number_of_presence_map


def draw_day_number_of_participants_map(day_number_of_participants_map):
    plot_label = 'partecipanti_per_lezione'

    pyplot.title(plot_label)

    fig, ax = pyplot.subplots(figsize=(50, 20))

    x_pos = numpy.arange(len(day_number_of_participants_map.keys()))

    ax.bar(x_pos, day_number_of_participants_map.values())
    ax.set_xticks(x_pos)
    ax.set_xticklabels(day_number_of_participants_map.keys())
    y_max = max(day_number_of_participants_map.values())
    ax.set_ylim(0, y_max)

    ax.tick_params('x', labelsize=20, labelrotation=90)
    ax.tick_params('y', labelsize=20)

    loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    finalize_plot('data', 'partecipanti', plot_label, 30)


def draw_participant_number_of_presence_map(participant_number_of_presence_map, x_max):
    plot_label = 'presenze_per_partecipante'

    pyplot.title(plot_label)

    fig, ax = pyplot.subplots(figsize=(50, 20))

    y_pos = numpy.arange(len(participant_number_of_presence_map.keys()))

    ax.barh(y_pos, participant_number_of_presence_map.values())
    ax.set_yticks(y_pos)
    ax.set_yticklabels(participant_number_of_presence_map.keys())
    ax.set_xlim(0, x_max)

    ax.tick_params('x', labelsize=20, labelrotation=90)
    ax.tick_params('y', labelsize=20)

    loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)

    finalize_plot('presenze', 'partecipante', plot_label, 30)


def finalize_plot(x_label, y_label, name, font_size):
  pyplot.grid()
  #pyplot.legend(loc='best')
  pyplot.xlabel(x_label, fontsize=font_size)
  pyplot.ylabel(y_label, fontsize=font_size)
  pyplot.savefig(name)
  pyplot.close()  # critical!
# END finalize_plot function


def sort_dictionary_by_value(orig_dict):
    sorted_dict = {}

    for k, v in sorted(orig_dict.items(), key=lambda item: item[1]):
        sorted_dict[k] = v
        #print(f'{k}: {v}')

    return sorted_dict


def main():
    global participants
    global participant_presences_map

    input_file_name = "results.txt"

    #print("opening", input_file_name)

    populate_participants()
    #print(participants)

    with open(input_file_name) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    day_participants_map = process(content)

    actual_day_participants_map = process_map(day_participants_map)

    json_string = json.dumps(actual_day_participants_map, default=set_default)
    print(json_string)

    day_number_of_participants_map = create_day_number_of_participants_map(actual_day_participants_map)
    #pprint.pprint(day_number_of_participants_map)
    # for k, v in sorted(day_number_of_participants_map.items(), key=lambda item: item[1]):
    #     print(f'{k}: {v}')

    draw_day_number_of_participants_map(day_number_of_participants_map)

    #pprint.pprint(participant_presences_map)

    participant_number_of_presence_map = create_participant_number_of_presence_map()
    #pprint.pprint(participant_number_of_presence_map)

    # for k, v in sorted(participant_number_of_presence_map.items(), key=lambda item: item[1], reverse=True):
    #     print(f'{k}: {v}')

    sorted_participant_number_of_presence_map = sort_dictionary_by_value(participant_number_of_presence_map)
    #pprint.pprint(sorted_participant_number_of_presence_map)

    x_max = len(day_number_of_participants_map.keys())
    draw_participant_number_of_presence_map(sorted_participant_number_of_presence_map, x_max)


if __name__ == "__main__":
    main()
