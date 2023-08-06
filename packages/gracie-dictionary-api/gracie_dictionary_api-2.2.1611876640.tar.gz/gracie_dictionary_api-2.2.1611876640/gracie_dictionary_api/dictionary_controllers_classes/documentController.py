from gracie_dictionary_api import GracieBaseAPI


class documentController(GracieBaseAPI):
    """Document Controller"""

    _controller_name = "documentController"

    def add(self, text, **kwargs):
        """

        Args:
            folderId: (string): Id is some of { topic, topic-type, skillset, skill, cluster set, cluster group, cluster, profile, profile-class }
            languageId: (string): languageId
            name: (string): name
            text: (type): text
            weight: (number): Document weight in range [-5,5]

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}, 'weight': {'name': 'weight', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFile(self, files, folderId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            files: (array): files
            folderId: (string): Id is some of { topic-type, skill, clusterset, cluster, profile, profile-class }
            languageId: (string): languageId
            splitByLines: (boolean): splitByLines

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'files': {'name': 'files', 'required': True, 'in': 'formData'}, 'folderId': {'name': 'folderId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'splitByLines': {'name': 'splitByLines', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/addFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, ids):
        """

        Args:
            ids: (array): ids

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): id
            name: (string): name
            text: (type): text
            weight: (number): Document weight in range [-5,5]

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': False, 'in': 'body'}, 'weight': {'name': 'weight', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            folderId: (string): Id is some of { topic, topic-type, skillset, skill, cluster set, cluster group, cluster, profile, profile-class }
            languageId: (string): * - request documents in all languages. For sorting folders by proximity user's language is used.
            limit: (integer): limit
            offset: (integer): offset
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): { "NONE", "NAME", "WEIGHT", "PROXIMITY", "DOC2VEC", "KEYWORDS", "ENTITIES" }

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
