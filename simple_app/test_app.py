from django.test import TestCase

class MyTestCase(TestCase):

    def test_get_posts(self):
        res0 = self.client.post('/users/', {'username': 'Sn7hySWymgOje25B2PRrwWxv4GTMGYz9h9vI0nJeY45VvMy1khLkmScA', 'email': 'phillip48@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'architecto reprehenderit elit. placeat modi', 'content': 'accusantium veniam esse culpa!', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.get('/posts/', {}, 'application/json')
        assert res2.status_code < 400

    def test_post_posts(self):
        res0 = self.client.post('/users/', {'username': 'DVcrSNYEYkY0h2m5PQBVybPSfOnXqOkZoRzye6qDd0', 'email': 'adamsjacob@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'esse', 'content': 'Lorem ipsum, culpa! culpa! officiis Hic veniam', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400

    def test_get_posts_detail(self):
        res0 = self.client.post('/users/', {'username': 'Foz6YWyyjSzDXMeEijMezRRWy', 'email': 'bernardbrittney@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'Hic modi magnam, elit. veniam accusantium odit', 'content': 'illum sit Lorem accusantium libero illum ipsum,', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.get(f"/posts/{res1.data['id']}/", {}, 'application/json')
        assert res2.status_code < 400

    def test_patch_posts_detail(self):
        res0 = self.client.post('/users/', {'username': 'upR4jG86uBnxSOJRwA1QjZnTsbpQ3FMgUEaIbKwmGW8gtZOq27VPPgmoNqeNUWLwPhcEN63aGw7I3kuAiIBQLBYq0ms7FKP', 'email': 'xjohnson@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'nobis libero molestias, Lorem dolor', 'content': 'esse', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.patch(f"/posts/{res1.data['id']}/", {}, 'application/json')
        assert res2.status_code < 400

    def test_delete_posts_detail(self):
        res0 = self.client.post('/users/', {'username': '3WUGuZsEKtguGt5', 'email': 'swarner@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'architecto molestias, modi libero reprehenderit', 'content': 'odit elit. possimus ipsum, accusantium officiis', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.delete(f"/posts/{res1.data['id']}/", {}, 'application/json')
        assert res2.status_code < 400

    def test_get_comments(self):
        res0 = self.client.post('/users/', {'username': 'Iy', 'email': 'tiffany64@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'reiciendis architecto architecto accusantium sit', 'content': 'architecto repellendus molestias, exercitationem', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'architecto repellendus molestias, exercitationem', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.get('/comments/', {}, 'application/json')
        assert res3.status_code < 400

    def test_post_comments(self):
        res0 = self.client.post('/users/', {'username': 'nzHaZ6JTnK9I2eom8qyzJ3i', 'email': 'alexanderrichard@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'adipisicing quas placeat libero', 'content': 'amet esse consectetur possimus repellendus amet', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'amet esse consectetur possimus repellendus amet', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400

    def test_get_comments_detail(self):
        res0 = self.client.post('/users/', {'username': 'e2zujyCU6OTdgZ5usobRUvZepnvfIBJwknv8LOKlyqg2cfhxumF7oSxGznbBdfI8EpKbn35AUbPP8knME7IxG3wNod', 'email': 'fhahn@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'Lorem accusantium', 'content': 'exercitationem adipisicing reiciendis Lorem dolor', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'exercitationem adipisicing reiciendis Lorem dolor', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.get(f"/comments/{res2.data['id']}/", {}, 'application/json')
        assert res3.status_code < 400

    def test_patch_comments_detail(self):
        res0 = self.client.post('/users/', {'username': 'CRioukDviZCBBrBax9RyFAedPCTp8NRo6ilk2P5bF3ECKK5V9ZXCcY0JGkcWpeDH58q7b8q9uYjKRRtLkVmZwIs0I24ggTJ6Np', 'email': 'eelliott@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'libero adipisicing', 'content': 'repellendus illum placeat Lorem placeat officiis', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'repellendus illum placeat Lorem placeat officiis', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.patch(f"/comments/{res2.data['id']}/", {'author': res2.data['author'], 'content': 'repellendus illum placeat Lorem placeat officiis', 'post': res2.data['post']}, 'application/json')
        assert res3.status_code < 400

    def test_delete_comments_detail(self):
        res0 = self.client.post('/users/', {'username': 'AqlwgZ7WC4bacELm4utJmSNvwtr29oABIbFFnWUIrNgPc0dXZyw8t1s1yeV7p', 'email': 'yblair@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'veniam sit reprehenderit adipisicing placeat quas', 'content': 'molestias,', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'molestias,', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.delete(f"/comments/{res2.data['id']}/", {}, 'application/json')
        assert res3.status_code < 400

    def test_get_users(self):
        res0 = self.client.post('/users/', {'username': 'sr9JrDECk7sOB5jBJJuZ5eW1huBzegX7lxEpz', 'email': 'dorothyhale@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.get('/users/', {}, 'application/json')
        assert res1.status_code < 400

    def test_post_users(self):
        res0 = self.client.post('/users/', {'username': '8HmlKmEe9K3mcjMgAKqGrnK4BWORL092WqIEE9O6kGormeixtSuVKiBs5yAvtGTqYm1uTJ4qtO9l0J', 'email': 'barberemma@example.org'}, 'application/json')
        assert res0.status_code < 400

    def test_get_users_detail(self):
        res0 = self.client.post('/users/', {'username': 'V3NKwhNQX8AfSTqc6fex746BbkzdAu5OBKwvyze657Rl1dGdCJ0GgzX', 'email': 'lindamckay@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.get(f"/users/{res0.data['id']}/", {}, 'application/json')
        assert res1.status_code < 400

    def test_patch_users_detail(self):
        res0 = self.client.post('/users/', {'username': 'RkdMgZhXWx', 'email': 'jeremiah07@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.patch(f"/users/{res0.data['id']}/", {}, 'application/json')
        assert res1.status_code < 400

    def test_delete_users_detail(self):
        res0 = self.client.post('/users/', {'username': 'BIflR4tnBKfnGREAVf9cGk5l2IFDenj3JGLry9scM7turL33lyHQrpcyAPLptqN', 'email': 'jose26@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.delete(f"/users/{res0.data['id']}/", {}, 'application/json')
        assert res1.status_code < 400