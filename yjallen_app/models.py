from django.utils.safestring import mark_safe
from django.db import models
from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml import xmlmap
from eulxml.xmlmap.core import XmlObject
#from eulxml.xmlmap.dc import DublinCore
from eulxml.xmlmap.fields import StringField, NodeField, StringListField, NodeListField, IntegerField
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

class LetterTitle(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('/tei:TEI')
    id = StringField('@xml:id')
    text = StringField('tei:text')
    date =  StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title/tei:date')
    title = StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title')
    author =  StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:name/tei:choice/tei:reg')

    site_url = 'http://beck.library.emory.edu/yjallen'
    project_desc = StringField('tei:teiHeader/tei:encodingDesc/tei:projectDesc')
    geo_coverage = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type="geography"]')
    creation_date = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:date')
    lcsh_subjects = StringListField('tei:teiHeader//tei:keywords[@scheme="#lcsh"]/tei:list/tei:item')
    identifier_ark = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type="ark"]')
    source = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc')

'''
    @property
    def dublin_core(self):
        dc = DublinCore()
        dc.title = self.title
        dc.creator_list.extend([n.reg for n in self.header.author_list])
        dc.contributor_list.extend([n.reg for n in self.header.editor_list])
        dc.publisher = self.header.publisher
        dc.date = self.header.publication_date
        dc.rights = self.header.availability
        dc.source = self.header.source_description
        dc.subject_list.extend(self.lcsh_subjects)
        dc.description = self.project_desc

        dc.identifier = self.identifier_ark


        if self.geo_coverage:
            dc.coverage_list.append(self.geo_coverage)
        if self.creation_date:
            dc.coverage_list.append(self.creation_date)

        if self.header.series_statement:
            dc.relation_list.append(self.header.series_statement)
        # FIXME: should we also include url? site name & url are currently
        # hard-coded when setting dc:relation in postcard ingest

        return dc
'''

class Letter(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE} 
    objects = Manager("//tei:text")
    letter_doc = NodeField('ancestor::tei:TEI', LetterTitle)
            
    
  
