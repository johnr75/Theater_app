from bson import ObjectId
from datetime import datetime, time
from .extensions import mongo


def db_open_record(db, pid):
    output = db.find_one({"_id": ObjectId(pid)})
    return output


def db_add_record(db, form):
    comp = db_open_record(mongo.db.Company, form.company.data)
    add_items = ({'Production': form.production.data,
                  'Company': {
                      'Name': comp['Name'],
                      'City': comp['City'],
                      'State': comp['State'],
                      'Type': comp['Type']
                  },
                  'Show Open': datetime.combine(form.show_open.data, time()),
                  'Number of Shows': form.shows.data,
                  'Production Type': form.s_type.data})
    newid = db.insert_one(add_items)
    return newid.inserted_id


def db_edit_record(db, form, pid):
    comp = db_open_record(mongo.db.Company, form.company.data)

    edit_items = ({'Production': form.production.data,
                   'Company': {
                       'Name': comp['Name'],
                       'City': comp['City'],
                       'State': comp['State'],
                       'Type': comp['Type']
                   },
                   'Show Open': datetime.combine(form.show_open.data, time()),
                   'Number of Shows': form.shows.data,
                   'Production Type': form.s_type.data})
    db.update_one({'_id': ObjectId(pid)}, {"$set": edit_items}, upsert=False)
    return pid


def db_add_cc(db, form, pid):
    new_item = {'Type': form.type.data,
                'Person': form.person.data,
                'Role': form.role.data}
    print(new_item)
    rs = db.update_one({'_id': ObjectId(pid)}, {'$push': {'Cast_Crew': new_item}})
    print(rs)
    return pid


def db_remove_cc(db, role, name, pid):
    rs = db.update_one({'_id': ObjectId(pid)}, {'$pull': {'Cast_Crew': {'Person': name, 'Role': role}}})
    print(rs.modified_count, 'record were updated')
    return rs


def db_pull_list(db):
    output = [x for x in db.find()]
    return output


def db_edit_utility_list(db, form, pid):
    edit_items = ({'Name': form.name.data, 'Active': form.active.data})
    db.update_one({'_id': ObjectId(pid)}, {"$set": edit_items}, upsert=False)
    return pid


def db_add_utility_list(db, form):
    add_items = ({'Name': form.name.data, 'Active': form.active.data})
    newid = db.insert_one(add_items)
    return newid.inserted_id


def db_edit_company_list(db, form, pid):
    edit_items = ({'Name': form.company.data,
                   'Active': form.active.data,
                   'City': form.city.data,
                   'State': form.state.data,
                   'Type': form.c_type.data})
    db.update_one({'_id': ObjectId(pid)}, {"$set": edit_items}, upsert=False)
    return pid


def db_add_company_list(db, form):
    add_items = ({'Name': form.company.data,
                  'Active': form.active.data,
                  'City': form.city.data,
                  'State': form.state.data,
                  'Type': form.c_type.data})
    newid = db.insert_one(add_items)
    return newid.inserted_id

