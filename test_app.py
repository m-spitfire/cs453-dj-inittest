from django.test import TestCase

class MyTestCase(TestCase):

    def test_get_posts(self):
        res0 = self.client.post('/users/', {'username': 'pkcgm1OYtGJMJCMNKDCy3FZMzZPWSvBwCmG4', 'email': 'pallison@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'culpa! repellendus ipsum esse adipisicing nobis', 'content': 'quas consectetur ipsum, ipsum, Hic architecto Hic', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.get('/posts/', {}, 'application/json')
        assert res2.status_code < 400

    def test_post_posts(self):
        res0 = self.client.post('/users/', {'username': 'NGBWTiOat318g90rwc5kab6CyPcnbniF9dnfSTC62KZMmg9l6AYE3U3hWRFs3adQ4fVcXznkXAgnGbU9Xqm0i3', 'email': 'parker69@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'exercitationem elit. reiciendis accusantium ipsum', 'content': 'Lorem magnam, elit. Lorem modi odit dolor veniam', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400

    def test_get_posts_detail(self):
        res0 = self.client.post('/users/', {'username': 'bS64yLBWOrzAoiB4cqmuL2vKK2aDEJBIyT27Cclr5FP7ExmyClHFaIYc835qOf2hbq3DUuMGYLN', 'email': 'james76@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'reiciendis', 'content': 'exercitationem consectetur nobis ipsum, nobis sit', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.get(f"/posts/{res1.data['id']}/", {}, 'application/json')
        assert res2.status_code < 400

    def test_patch_posts_detail(self):
        res0 = self.client.post('/users/', {'username': 'DlyKX6KRneQ63VGA0R5QSAJzjllfZQWaFNinyF8n1Z7kL1nXr9CtnmOsDkmfmQNxl', 'email': 'yolanda74@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'repellendus', 'content': 'culpa! ipsum, reprehenderit architecto officiis', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.patch(f"/posts/{res1.data['id']}/", {'content': 'culpa! ipsum, reprehenderit architecto officiis'}, 'application/json')
        assert res2.status_code < 400

    def test_delete_posts_detail(self):
        res0 = self.client.post('/users/', {'username': 'LwBpPuDrzuzj94PUXK0iTWLPx4I6Ye6IMHOJbZoYV58l6k2OEzg8b1s8NM5uqJvJOrt0FzdzxNkF7ucHCRv', 'email': 'tylerpatterson@example.com'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'possimus exercitationem quas Lorem odit officiis', 'content': 'placeat veniam consectetur adipisicing officiis', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.delete(f"/posts/{res1.data['id']}/", {}, 'application/json')
        assert res2.status_code < 400

    def test_get_comments(self):
        res0 = self.client.post('/users/', {'username': 'M3ieFgOIqtwYl6FLde9l2gTjLohu7ls9PKdUuD1bSz58sPTH1wBGhQtT6', 'email': 'moorejoseph@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'Hic', 'content': 'Hic adipisicing Hic placeat placeat odit elit.', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'Hic adipisicing Hic placeat placeat odit elit.', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.get('/comments/', {}, 'application/json')
        assert res3.status_code < 400

    def test_post_comments(self):
        res0 = self.client.post('/users/', {'username': 'FBfuI', 'email': 'orosario@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'exercitationem odit molestias, dolor accusantium', 'content': 'reiciendis consectetur officiis magnam, elit. sit', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'reiciendis consectetur officiis magnam, elit. sit', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400

    def test_get_comments_detail(self):
        res0 = self.client.post('/users/', {'username': '5KIrlbIxhF5hAKrr0LNAzIwFL0pKmP1iZzA8mi9aDBQCR54p65ONB5PVsmEDcPsP8go5Un', 'email': 'brittany59@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'amet esse possimus esse esse molestias, Lorem Hic', 'content': 'modi modi sit adipisicing accusantium Hic ipsum', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'modi modi sit adipisicing accusantium Hic ipsum', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.get(f"/comments/{res2.data['id']}/", {}, 'application/json')
        assert res3.status_code < 400

    def test_patch_comments_detail(self):
        res0 = self.client.post('/users/', {'username': 'YAsfVlnuxjTwIo1sUyO3Pvf1eyjIqhrurm9byXDrCcGeVVQsIwOQM6l5In0PdBE6caTaiRKcrHCUh9PWAmVqX3cGmB0D', 'email': 'davidgreene@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'repellendus adipisicing architecto sit nobis', 'content': 'veniam elit. veniam culpa! reiciendis amet amet', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'veniam elit. veniam culpa! reiciendis amet amet', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.patch(f"/comments/{res2.data['id']}/", {'author': res2.data['author'], 'content': 'veniam elit. veniam culpa! reiciendis amet amet', 'post': res2.data['post']}, 'application/json')
        assert res3.status_code < 400

    def test_delete_comments_detail(self):
        res0 = self.client.post('/users/', {'username': '0cGXalQgV8jzXPCghBGq8nGLNUTuspA80lFRNghS3Vy4O3Db0sj2s6besaVf', 'email': 'vking@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.post('/posts/', {'title': 'consectetur sit accusantium Lorem ipsum, quas Hic', 'content': 'officiis Lorem magnam, esse officiis magnam,', 'author': res0.data['id']}, 'application/json')
        assert res1.status_code < 400
        res2 = self.client.post('/comments/', {'author': res1.data['author'], 'content': 'officiis Lorem magnam, esse officiis magnam,', 'post': res1.data['id']}, 'application/json')
        assert res2.status_code < 400
        res3 = self.client.delete(f"/comments/{res2.data['id']}/", {}, 'application/json')
        assert res3.status_code < 400

    def test_get_users(self):
        res0 = self.client.post('/users/', {'username': '1O2Q6v4pfdZ7ooKLALv', 'email': 'williammercado@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.get('/users/', {}, 'application/json')
        assert res1.status_code < 400

    def test_post_users(self):
        res0 = self.client.post('/users/', {'username': 'Kt2x2wJoG5lfsxos5Lew5SN6RpuTwkK5ONvQlxqBGiUFepw7b3C44mqbam5SPzVmRm4Ky1', 'email': 'jeffreymann@example.net'}, 'application/json')
        assert res0.status_code < 400

    def test_get_users_detail(self):
        res0 = self.client.post('/users/', {'username': '16mfyoN99IG8JOWgEj7HQEOoMIc4qw3ZdF6LVl3xeF0LQidBAplLBkNoEY0ULwB', 'email': 'garciabrian@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.get(f"/users/{res0.data['id']}/", {}, 'application/json')
        assert res1.status_code < 400

    def test_patch_users_detail(self):
        res0 = self.client.post('/users/', {'username': '0m8zMHyrM8GV6qkUZrsjJkBS3NFuyrikFEsRzTbbF5RLaMEbQjG2s78Q1AcifnAdd', 'email': 'jgardner@example.org'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.patch(f"/users/{res0.data['id']}/", {'email': 'jgardner@example.org'}, 'application/json')
        assert res1.status_code < 400

    def test_delete_users_detail(self):
        res0 = self.client.post('/users/', {'username': 'ZiAGSywH8rKzpg9X2ZS6Z5gKX82F7', 'email': 'rarmstrong@example.net'}, 'application/json')
        assert res0.status_code < 400
        res1 = self.client.delete(f"/users/{res0.data['id']}/", {}, 'application/json')
        assert res1.status_code < 400