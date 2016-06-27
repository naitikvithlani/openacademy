# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    parent_course_id =  fields.Many2one('openacademy.course',
                                 ondelete='set null', string="Parent course")


    @api.model
    def name_search(self, name, args=None, operator='like', limit=100):
        args = args or []
	rec_list = []
        recs = self.browse()
	res = re.compile('^([A-Za-z0-9][A])')
	result = res.match(name)
	
        if name and result:
            recs = self.search([('name', '=', name)] + args, limit=limit)
	if name and result and not recs:
	    recs = self.search([('name', 'like', name)] + args, limit=limit)
	if not name:
	    recs = self.search([] + args, limit=limit)
   	    for rec in recs:
		matched_rec = res.match(rec.name)
		if matched_rec:
		    rec_list.append(rec.id)
	    recs = self.browse(rec_list)
        return recs.name_get()
