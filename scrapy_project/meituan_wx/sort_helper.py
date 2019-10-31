#!/usr/bin/env python
# coding:utf-8


def handle_sort_distace(shop_distances_list):
    list = []
    for distance in shop_distances_list:
        distance = str(distance)
        if 'km' in distance:
            distance = eval(distance.replace('km', '')) * 1000
            list.append(int(distance))
        else:
            distance = eval(distance.replace('m', ''))
            list.append(distance)
    print list
    if list == sorted(list):
        return True
    else:
        return False


def handle_sort_distace_2(shop_distances_list):
    list = []
    for distance in shop_distances_list:
        distance = str(distance)
        if 'km' in distance:
            distance = eval(distance.replace('km', '')) * 1000
            list.append(int(distance))
        else:
            distance = eval(distance.replace('m', ''))
            list.append(distance)
    return list


