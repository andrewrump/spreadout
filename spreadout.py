#!/usr/bin/python3
#
# Spreadout JSON or XML and dump all attributes
#
# BUGS
#
# TODO
#
# DONE
#

import argparse
import re
import json
#import xmltodict
#try:
#  from lxml import etree
#  print("running with lxml.etree")
#except ImportError:
#  try:
#    # Python 2.5
#    import xml.etree.cElementTree as etree
#    print("running with cElementTree on Python 2.5+")
#  except ImportError:
#    try:
#      # Python 2.5
#      import xml.etree.ElementTree as etree
#      print("running with ElementTree on Python 2.5+")
#    except ImportError:
#      try:
#        # normal cElementTree install
#        import cElementTree as etree
#        print("running with cElementTree")
#      except ImportError:
#        try:
#          # normal ElementTree install
#          import elementtree.ElementTree as etree
#          print("running with ElementTree")
#        except ImportError:
#          print("Failed to import ElementTree from any known place")
import xml.etree.ElementTree as ET
import xml.dom.minidom

def spreadout_json(args, json_object, path = ''):
   if type(json_object) == str:
      if args.value:
         print(path, json_object)
      else:
         print(path)
   elif type(json_object) == dict:
      for key in json_object:
         value = json_object[key]
         if type(value) == str:
            if args.value:
               print(path + '>' + key, value)
            else:
               print(path + '>' + key)
         elif type(value) == dict:
            print(path + '>' + key + '>')
            spreadout_json(args, json_object[key], path + '>' + key)
         elif type(value) == list:
            print(path + '>' + key + '>')
            spreadout_json(args, json_object[key], path + '>' + key)
         elif type(value) == int:
            if args.value:
               print(path + '>' + key, '<int>')
            else:
               print(path + '>' + key)
         elif value == None:
            if args.value:
               print(path + '>' + key, '<None>')
            else:
               print(path + '>' + key)
         else:
            raise Exception(path + '>' + key + '(' + str(type(value)))
   elif type(json_object) == list:
      for key in json_object:
         spreadout_json(args, key, path)
   else:
      raise Exception(path + '(' + str(type(json_object)))

def read_json(args):
   file = open(args.file)
   json_object = json.load(file)
   file.close()
   spreadout_json(args, json_object)

def spreadout_xml(args, xml_object, path = ''):
   print(type(xml_object))
   for child in xml_object:
      print(type(child))
      print(child.text)

def Yspreadout_xml(args, xml_object, path = ''):
   print('X ', type(xml_object))
   if type(xml_object) == str:
      print('A ', path, xml_object)
   else:
      for child in xml_object:
         if type(child) == str:
            print('B ', path, child)
         elif type(child.tag) == str:
            #print('Y ', child.text.strip())
            print('C ',path, type(child.tag), child.tag, type(child.attrib), child.attrib)
            if type(child.attrib) == dict:
               spreadout_xml(args, child.attrib, path + '>' + child.tag)
            else:
               raise Exception(path + '>' + child.tag)
         else:
            raise Exception(path + '(' + str(type(child.tag)))
       #else:
       #   print(path, type(child.tag))
       #   print(path, type(child.tag))
       #   if type(child.tag) == dict:
       #      print(path + '>' + child.tag + '>')
       #      spreadout_xml(args, child.tag, path + '>' + child.tag)
       #   else:
       #      print('x', path, child.tag, child.tag)
       #      exit()
   #print('<')

def Xspreadout_xml(args, xml_object, path = ''):
   #print(type(xml_object))
   for child in xml_object:
       if type(child) == str:
          print(path, child)
       elif type(child.tag) == str:
          print(path, child.tag)
          if type(child.attrib) == dict:
             spreadout_xml(args, child.attrib, path + '>' + child.tag)
          else:
             print('y', path, type(child.attrib))
             exit()
       else:
          print(path, type(child.tag))
          print(path, type(child.attrib))
          if type(child.attrib) == dict:
             print(path + '>' + child.tag + '>')
             spreadout_xml(args, child.attrib, path + '>' + child.tag)
          else:
             print('x', path, child.tag, child.attrib)
             exit()
   #print('<')

def read_xml(args):
   tree = ET.parse(args.file)
   root = tree.getroot()
   spreadout_xml(args, root)

def Zread_xml(args):
   root = xml.dom.minidom.parse(args.file).documentElement
   spreadout_xml(args, root)

def json_xml_type(arg_value, pat = re.compile(r"^[jJXx]$")):
   if not pat.match(arg_value):
      raise argparse.ArgumentTypeError
   return arg_value

def main():
   parser = argparse.ArgumentParser(description = 'Decompose JSON and XML files')
   parser.add_argument('-t', '--type', required = True, type = json_xml_type, help = 'JSON (j) og XML (x)')
   parser.add_argument('-f', '--file', required = True, help = 'Input file')
   parser.add_argument('-v', '--value', action = 'store_true', help = 'print values')
   #parser.add_argument('--sum', dest='accumulate', action='store_const',
   #                 const=sum, default=max,
   #                 help='sum the integers (default: find the max)')
   args = parser.parse_args()
   try:
      if args.type.upper() == 'J':
         read_json(args)
      else:
         read_xml(args)
   except FileNotFoundError:
      print(args.file, 'not found')
   except json.decoder.JSONDecodeError:
      print(args.file, 'not JSON')

if __name__ == "__main__":
   main()
