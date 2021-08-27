import os, json

class Cache:
    def __init__(self, config_folder):
        self.config_folder = config_folder


    def get_cache(self, entity, cache = True):
        entity_type = entity['type'] or None
        entity_path = entity['path'] or ''
        get_entities = entity['get'] or None
        
        if not entity_type or not get_entities:
            raise ValueError(f"Can't load data. entity_type or load method not provided")
 

        self.cache_path_folder = self.get_cache_file_folder(entity_path)
        cache_path_file = self.get_cache_file_path(entity_type, entity_path)

        if cache:
            try:
                result =  self.get(cache_path_file, get_entities) 
            except Exception as e:
                print('Exception', e)
                pass   
        else:
            result = get_entities()
            self.save(self.cache_path_folder , cache_path_file, result)
        if len(result) == 0:
            print(f"No {entity_type}")
        return result


    def update_cache(self, entity_type, entity_path, data):
        cache_path_file = os.path.join(
            self.config_folder, 'cache', entity_path, f"{entity_type}.json"
        )
        self.save(self.cache_path_folder, cache_path_file, data)


    def get(self, cache_path_file, callback):
        if os.path.exists(cache_path_file):
            return self.get_cache_file(cache_path_file)
        else:
            result = callback()
            self.save(self.cache_path_folder, cache_path_file, result)
            return result

    
    def get_cache_file(self, cache_path_file):
        if os.path.exists(cache_path_file):
            with open(cache_path_file) as json_file:
                return json.load(json_file)        
        return None


    def get_cache_file_folder(self, entity_path):
        return os.path.join(
            self.config_folder, 'cache', entity_path
        )

    def get_cache_file_path(self, entity_type, entity_path):
        return os.path.join(
            self.config_folder, 'cache', entity_path, f"{entity_type}.json"
        )       

    def save(self, cache_path_folder, cache_path_file, data):
        if not os.path.isdir(cache_path_folder):
            os.makedirs(cache_path_folder)
        self.save_file(data, cache_path_file)


    def save_file(self, obj, filename):
        json.dump(obj, open(filename, "w"))