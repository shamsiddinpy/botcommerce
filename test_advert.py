# from urllib.parse import urlencode
#
# import pytest
# from rest_framework.reverse import reverse_lazy
#
# from adverts.models import Advert
#
#
# class TestAdvert:
#     @pytest.mark.django_db
#     def test_create_advert(self, api_client, load_region_district, login, advert, user):
#         url = reverse_lazy('adverts:advert-list')
#         data = {
#             "name": "string",
#             "type": "job",
#             "region": 14,
#             "district": 161,
#             "job_type": "one-time",
#             "working_days": [
#                 1
#             ],
#             "from_time": "string",
#             "to_time": "string",
#             "from_sum": 10000,
#             "to_sum": 1000000,
#             "is_negotiate": True,
#             "from_age": 18,
#             "to_age": 50,
#             "is_has_diploma": True,
#             "university": "string",
#             "about": "string",
#             "achievement": "string",
#             "addition_number": user.phone_number,
#             "experience": "optional",
#             "status": "unemployed",
#             "sex": "woman",
#             "keyword": [
#                 "string"
#             ],
#             "is_top": True
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == 201
#         res_data = response.data
#         assert res_data['name'] == advert.name
#         assert res_data['type'] == advert.type
#         assert res_data['addition_number'] == advert.addition_number
#         assert res_data['sex'] == advert.sex
#         assert advert.author_id == user.id
#         assert advert.author.phone_number == user.phone_number
#         assert advert.author.role == user.role
#
#     @pytest.mark.django_db
#     def test_advert_list(self, api_client, advert):
#         url = reverse_lazy('adverts:advert-advert')
#         response = api_client.get(url)
#         assert response.status_code == 200
#
#     @pytest.mark.django_db
#     def test_advert_list_path(self, api_client, advert):
#         base_url = reverse_lazy('adverts:advert-advert')
#         query = {
#             'search': "string",
#             # 'from_age__gte': 18,
#             # 'to_age__lte': 50,
#             # 'from_sum__gte': 10000,
#             # 'to_sum__lte': 100000,
#             'district': 161,
#             'region': 14,
#             # 'is_has_diploma': True,
#             'sex': 'woman',
#             # 'job_type': 'one-time',
#             # 'keyword': 'math',
#             # 'working_days': 2,
#             # 'page': '1',
#             # 'page_size': '100',
#         }
#         url = f"{base_url}?{urlencode(query)}"
#         response = api_client.get(url)
#         results = response.data['results']
#         assert response.status_code == 200
#         assert results[0]['name'] == query['search'] or results[0]['about'] == query['search'] or results[0][
#             'keyword'] == query['search']
#
#         assert results[0]['sex'] == query['sex']
#         assert results[0]['region'] == query['region']
#         assert results[0]['district'] == query['district']
#
#     @pytest.mark.django_db
#     def test_favorite_adverts_list(self, api_client, login, advert_favorite):
#         url = reverse_lazy('adverts:advert-favorite-adverts')
#         response = api_client.get(url)
#         assert response.status_code == 200
#         data = response.data['results'][0]
#         assert data['is_saved']
#
#     @pytest.mark.django_db
#     def test_favorite_resumes_list(self, api_client, login, resume_favorite):
#         url = reverse_lazy('adverts:advert-favorite-resumes')
#         response = api_client.get(url)
#         assert response.status_code == 200
#         data = response.data['results'][0]
#         assert data['is_saved']
#
#     # TODO I don't understand my notification   @pytest.mark.django_db
#     def test_my_notification(self, api_client, login, notification):
#         url = reverse_lazy('adverts:advert-get-notification')
#         response = api_client.get(url)
#         assert response.status_code == 200
#
#     @pytest.mark.django_db
#     def test_resume_create(self, api_client, login, load_region_district, user):
#         url = reverse_lazy('adverts:resume')
#         data = {
#             'name': "string",
#             'type': Advert.Type.RESUME,
#             'region_id': 14,
#             'full_name': "string",
#             'district_id': 161,
#             'birth_date': "2023-06-19",
#             'job_type': Advert.JobType.ONE_TIME,
#             'working_days': [
#                 1, 2
#             ],
#             'from_time': "string",
#             'to_time': "string",
#             'from_sum': 10000,
#             'to_sum': 10000,
#             'is_negotiate': True,
#             'from_age': 18,
#             'to_age': 30,
#             'is_has_diploma': True,
#             'university': "string",
#             'about': "string",
#             'achievement': "string",
#             'addition_number': user.phone_number,
#             'experience': "optional",
#             'status': "unemployed",
#             'sex': "woman",
#             'keyword': [
#                 "string"
#             ],
#             'is_top': True
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == 201
#         res_data = response.data
#         resume = Advert.objects.first()
#         assert res_data['id'] == resume.id
#         assert res_data['type'] == resume.type
#
#     @pytest.mark.django_db
#     def test_resume_list(self, api_client, resume):
#         url = reverse_lazy('adverts:advert-resume')
#         response = api_client.get(url)
#         assert response.status_code == 200
#
#         data = response.data['results'][0]
#         resume = Advert.objects.first()
#         assert data['id'] == resume.id
#         assert data['type'] == resume.type
#
#     @pytest.mark.django_db
#     def test_resume_list_path(self, api_client, resume):
#         base_url = reverse_lazy('adverts:advert-resume')
#         query = {
#             'search': "string",
#             # 'from_age__gte': 18,
#             # 'to_age__lte': 50,
#             # 'from_sum__gte': 10000,
#             # 'to_sum__lte': 100000,
#             'district': 161,
#             'region': 14,
#             # 'is_has_diploma': True,
#             'sex': 'woman',
#             # 'job_type': 'one-time',
#             # 'keyword': 'math',
#             # 'working_days': 2,
#             # 'page': '1',
#             # 'page_size': '100',
#         }
#         url = f"{base_url}?{urlencode(query)}"
#         response = api_client.get(url)
#         assert response.status_code == 200
#         data = response.data['results'][0]
#         resume = Advert.objects.first()
#         assert data['id'] == resume.id
#         assert data['type'] == resume.type
#
#     @pytest.mark.django_db
#     def test_top_advert(self, api_client, advert):
#         url = reverse_lazy('adverts:advert-top-advert')
#         response = api_client.get(url)
#         assert response.status_code == 200
#         assert len(response.data) != 0 and response.data[0]['is_top']
#
#     @pytest.mark.django_db
#     def test_advert_read(self, api_client, login, advert):
#         url = reverse_lazy('adverts:advert-detail', kwargs={'pk': advert.id})
#         response = api_client.get(url)
#         assert response.status_code == 200
#         assert response.data['id'] == advert.id
#
#     @pytest.mark.django_db
#     def test_advert_update(self, api_client, login, load_region_district, advert, user):
#         url = reverse_lazy('adverts:advert-detail', kwargs={'pk': advert.id})
#
#         data = {
#             "name": "yangilandi",
#             "type": "job",
#             "region_id": 14,
#             "district_id": 162,
#             "job_type": "one-time",
#             "working_days": [
#                 1, 2, 3, 4
#             ],
#             "from_time": "string",
#             "to_time": "string",
#             "from_sum": 1000,
#             "to_sum": 10000,
#             "is_negotiate": True,
#             "from_age": 19,
#             "to_age": 29,
#             "is_has_diploma": True,
#             "university": "string",
#             "about": "string",
#             "achievement": "string",
#             "addition_number": user.phone_number,
#             "experience": "optional",
#             "status": "unemployed",
#             "sex": "man",
#             "keyword": [
#                 "string"
#             ],
#             "is_top": True
#         }
#         response = api_client.put(url, data)
#         assert response.status_code == 200
#         assert response.data['name'] == data['name']
#         assert response.data['region'] == data['region_id']
#         assert response.data['sex'] == data['sex']
#
#     @pytest.mark.django_db
#     def test_advert_delete(self, api_client, login, load_region_district, advert):
#         url = reverse_lazy('adverts:advert-detail', kwargs={'pk': advert.id})
#         response = api_client.delete(url)
#         assert response.status_code == 204
#         assert Advert.objects.first() is None
#
#     @pytest.mark.django_db
#     def test_add_favorite(self, api_client, login, advert):
#         url = reverse_lazy('adverts:advert-add-advert-favorite', kwargs={'pk': advert.id})
#         response = api_client.get(url)
#         assert response.status_code == 200
#         assert response.data['success']
#
#     @pytest.mark.django_db
#     def test_delete_favorite(self, api_client, login, advert_favorite, advert):
#         url = reverse_lazy('adverts:advert-delete-favorite', kwargs={'pk': advert.id})
#         response = api_client.delete(url)
#         assert response.status_code == 204
#         assert response.data['success']
#
#     @pytest.mark.django_db
#     def test_advert_rating(self, api_client, rate, login, advert):
#         url = reverse_lazy('adverts:advert-rating', kwargs={'pk': advert.id})
#         response = api_client.get(url)
#         assert response.status_code == 200
#         results = response.data['results'][0]
#         assert results['id'] == rate.id
#         assert results['advert'] == rate.advert_id
