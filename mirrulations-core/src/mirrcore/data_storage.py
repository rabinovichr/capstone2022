import pymongo


class DataStorage:
    def __init__(self):
        database = pymongo.MongoClient('mongo', 27017)['mirrulations']
        self.dockets = database['dockets']
        self.documents = database['documents']
        self.comments = database['comments']
        self.attachments = database['attachments']

    def exists(self, search_element):
        result_id = search_element['id']

        return self.dockets.count_documents({'id': result_id}) > 0 or \
            self.documents.count_documents({'id': result_id}) > 0 or \
            self.comments.count_documents({'id': result_id}) > 0 or \
            self.attachments.count_documents({'id': result_id}) > 0

    def add(self, data):
        if 'type' in data['data'].keys() and 'attachments_text' not in data['data'].keys():
            if data['data']['type'] == 'dockets':
                self.dockets.insert_one(data)
            elif data['data']['type'] == 'documents':
                self.documents.insert_one(data)
            elif data['data']['type'] == 'comments':
                self.comments.insert_one(data)
        elif 'attachments_text' in data['data'].keys():
            self.attachments.insert_one(data)
            # Use this code maybe for inserting multiple attachments 
            # into different mongo entries:
            # for i, attachment in enumerate(data['data']['attachments_text']):
            #     self.attachments.insert_one({'attachment'+str(i):attachment})