import requests, json

class ProjectPeriod(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        r = requests.get(self.url + "/api/users/?format=json", auth=(self.username, self.password))
        if r.status_code != 200:
            raise Exception('Login failed: ' + r.status_code, r.content)

    def get_customers(self):
        r = requests.get(self.url + "/api/customers/?format=json", auth=(self.username, self.password))
        data = json.loads(r.content)

        if not isinstance(data, list):
            data2 = data
            data = []
            data.append(data2)

        #print(data[0]['city'])
        return data

    def get_customer(self, id):
        r = requests.get(self.url + "/api/customers/" + str(id) + "?format=json", auth=(self.username, self.password))
        data = []
        data.append(json.loads(r.content))

        return data

    def add_customer(self, name, street, postcode, city, country, status):
        payload = {
                "name": name,
                "street": street,
                "postcode": str(postcode),
                "city": city,
                "country": country,
                "status": str(status)
            }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/api/customers/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 201:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

        return json.loads(r.content)['id']

    def mod_customer(self, id, name, street, postcode, city, country, status):
        payload = {
                "id": str(id),
                "name": name,
                "street": street,
                "postcode": str(postcode),
                "city": city,
                "country": country,
                "status": str(status)
            }
        headers = {'content-type': 'application/json'}
        r = requests.put(self.url + '/api/customers/' + str(id) + '/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 200:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def del_customer(self, id):
        headers = {'content-type': 'application/json'}
        r = requests.delete(self.url + '/api/customers/' + str(id) + '/?format=json', headers=headers, auth=(self.username, self.password))

        if r.status_code != 204:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def get_locations(self):
        r = requests.get(self.url + "/api/locations/?format=json", auth=(self.username, self.password))
        data = json.loads(r.content)

        if not isinstance(data, list):
            data2 = data
            data = []
            data.append(data2)

        return data

    def get_location(self, id):
        r = requests.get(self.url + "/api/locations/" + str(id) + "?format=json", auth=(self.username, self.password))
        data = []
        data.append(json.loads(r.content))

        return data

    def add_location(self, name, street, postcode, city, country, customer, status):
        payload = {
                "name": name,
                "street": street,
                "postcode": str(postcode),
                "city": city,
                "country": country,
                "customer": str(customer),
                "status": str(status)
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/api/locations/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 201:
            print(r.content)
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def mod_location(self, id, name, street, postcode, city, country, customer, status):
        payload = {
                "id": str(id),
                "name": name,
                "street": street,
                "postcode": str(postcode),
                "city": city,
                "country": country,
                "customer": str(customer),
                "status": str(status)
        }
        headers = {'content-type': 'application/json'}
        r = requests.put(self.url + '/api/locations/' + str(id) + '/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 200:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def del_location(self, id):
        headers = {'content-type': 'application/json'}
        r = requests.delete(self.url + '/api/locations/' + str(id) + '/?format=json', headers=headers, auth=(self.username, self.password))

        if r.status_code != 204:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def get_projects(self):
        r = requests.get(self.url + "/api/projects/?format=json", auth=(self.username, self.password))
        data = json.loads(r.content)

        if not isinstance(data, list):
            data2 = data
            data = []
            data.append(data2)

        return data

    def get_project(self, id):
        r = requests.get(self.url + "/api/projects/" + str(id) + "?format=json", auth=(self.username, self.password))
        data = []
        data.append(json.loads(r.content))

        return data

    def add_project(self, name, description, responsible, customer, status, budget, billing, hourlyrate):
        payload = {
                "name": name,
                "description": description,
                "responsible": str(responsible),
                "customer": str(customer),
                "status": status,
                "budget": budget,
                "billing": str(billing),
                "hourly_rate": hourlyrate
            }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/api/projects/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 201:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def mod_project(self, id, name, description, responsible, customer, status, budget, billing, hourlyrate):
        payload = {
                "id": str(id),
                "name": name,
                "description": description,
                "responsible": str(responsible),
                "customer": str(customer),
                "status": status,
                "budget": budget,
                "billing": str(billing),
                "hourly_rate": hourlyrate
            }
        headers = {'content-type': 'application/json'}
        r = requests.put(self.url + '/api/projects/' + str(id) + '/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 200:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def del_project(self, id):
        headers = {'content-type': 'application/json'}
        r = requests.delete(self.url + '/api/projects/' + str(id) + '/?format=json', headers=headers, auth=(self.username, self.password))

        if r.status_code != 204:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def get_acquisitions(self):
        r = requests.get(self.url + "/api/acquisitions/?format=json", auth=(self.username, self.password))
        data = []
        data.append(json.loads(r.content))

        return data

    def get_acquisition(self, id):
        r = requests.get(self.url + "/api/acquisitions/" + str(id) + "?format=json", auth=(self.username, self.password))
        data = json.loads(r.content)

        if not isinstance(data, list):
            data2 = data
            data = []
            data.append(data2)

        return data

    def add_acquisition(self, user, start, end, project, location, comment):
        payload = {
                "user": user,
                "start": start,
                "end": end,
                "project": project,
                "location": str(location),
                "comment": comment
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + '/api/acquisitions/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 201:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def mod_acquisition(self, id, user, start, end, project, location, comment):
        payload = {
                "id": str(id),
                "user": user,
                "start": start,
                "end": end,
                "project": project,
                "location": str(location),
                "comment": comment
        }
        headers = {'content-type': 'application/json'}
        r = requests.put(self.url + '/api/acquisitions/' + str(id) + '/?format=json', data=json.dumps(payload), headers=headers, auth=(self.username, self.password))

        if r.status_code != 200:
            raise Exception('Action failed: ' + str(r.status_code), r.content)

    def del_acquisition(self, id):
        headers = {'content-type': 'application/json'}
        r = requests.delete(self.url + '/api/acquisitions/' + str(id) + '/?format=json', headers=headers, auth=(self.username, self.password))

        if r.status_code != 204:
            raise Exception('Action failed: ' + str(r.status_code), r.content)