class Platform():
	registry = {}

	def __init__(self, id, name, is_brand_missing_from_name, platform_family_id, platform_family_name, model_no, storage_capacity, description, disambiguation, relevance):
		self.id = id
		self.name = name
		self.is_brand_missing_from_name = is_brand_missing_from_name
		self.platform_family_id = platform_family_id
		self.platform_family_name = platform_family_name
		self.model_no = model_no
		self.storage_capacity = storage_capacity
		self.description = description
		self.disambiguation = disambiguation
		self.relevance = relevance
		self.editions = dict()

	def add_to_registry(self):
		Platform.registry[self.id] = self

	def add_edition(self, edition):
		if edition.id not in self.editions:
			self.editions[edition.id] = edition

	def get_all_editions(self):
		return self.editions.values()

	def get_all_editions_jsonified(self):
		jsonified_editions = []
		for edn in self.editions:
			jsonified_editions.append(edn.jsonify())
		return jsonified_editions

	def jsonify(self):
		return {
			'id': self.id,
			'name': self.name,
			'is_brand_missing_from_name': self.is_brand_missing_from_name,
			'model_no': self.model_no,
			'storage_capacity': self.storage_capacity,
			'description': self.description,
			'disambiguation': self.disambiguation,
			'relevance': self.relevance,
			'editions': self.get_all_editions_jsonified()
		}

	@classmethod
	def get_by_id(cls, platform_id):
		return cls.registry.get(platform_id)

	@classmethod
	def get_by_edition_id(cls, edition_id):
		for platform in cls.get_all():
			for edition in platform.editions:
				if edition == edition_id:
					return platform
		return None

	@classmethod
	def get_all(cls):
		return cls.registry.values()
