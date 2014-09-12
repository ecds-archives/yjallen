import re

from django.utils.safestring import mark_safe
from django.db import models
from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml import xmlmap
from eulxml.xmlmap.core import XmlObject
#from eulxml.xmlmap.dc import DublinCore
from eulxml.xmlmap.fields import StringField, NodeField, StringListField, NodeListField, IntegerField
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

class LetterTitle(XmlModel, XmlObject):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('/tei:TEI')
    id = StringField('@xml:id')
    text = StringField('tei:text')
    date =  StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title/tei:date')
    date_num =  StringField('//tei:titleStmt/tei:title/tei:date/@when')
    
    #year = StringField('substring(//tei:titleStmt/tei:title/tei:date/@when,1,4)')
    
    title = StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title')
    head = StringField('//tei:text/tei:body/tei:div/tei:head')
    author =  StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:name/tei:choice/tei:reg')
    contributor = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:p/tei:address/tei:addrLine')
    publisher = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher')
    rights = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:p')
    issued_date = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date')
    site_url = 'http://beck.library.emory.edu/yjallen'
    source_title = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title')
    project_desc = StringField('tei:teiHeader/tei:encodingDesc/tei:projectDesc')
    geo_coverage = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type="geography"]')
    creation_date = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:date')
    lcsh_subjects = StringListField('tei:teiHeader//tei:keywords[@scheme="#lcsh"]/tei:list/tei:item')
    identifier_ark = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type="ark"]')
    series = StringField('tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:title')
    source = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl')


class Letter(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE} 
    objects = Manager("//tei:text")
    letter_doc = NodeField('ancestor::tei:TEI', LetterTitle)
            
    
  
