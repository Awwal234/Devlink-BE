from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from ..models.link import Link

link_namespace = Namespace('devlinks', description="scheme for links")

link_model = link_namespace.model('DEVLINK', {
    'id': fields.Integer(),
    'platform': fields.String(required=True, description="link platform"),
    'link': fields.String(required=True, description='link url')
})

@link_namespace.route('/create_link')
class CREATELINK(Resource):
    @link_namespace.expect(link_model)
    @link_namespace.marshal_with(link_model)
    @jwt_required()
    def post(self):
        '''
            Create link
        '''
        data = request.get_json()
        platform = data['platform']
        link = data['link']

        link_exist = Link.query.filter_by(link=link).first()
        if link_exist:
            response = {
                'message': 'link already exist'
            }

            return response, HTTPStatus.UNAUTHORIZED
        else:
            new_link = Link(platform=platform, link=link)
            new_link.save()

            return new_link, HTTPStatus.CREATED

@link_namespace.route('/getlinks')
class GETLINKS(Resource):
    @link_namespace.marshal_with(link_model)
    @jwt_required()
    def get(self):
        '''
            Get all links
        '''
        
        links_for_user = Link.query.all()
        return links_for_user, HTTPStatus.OK