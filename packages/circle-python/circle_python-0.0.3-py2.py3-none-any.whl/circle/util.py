from circle.circle_response import CircleResponse


def convert_to_circle_object(response, api_key=None):

    # If a CircleResponse is passed, return the StripeObject associated with it.

    if isinstance(response, CircleResponse):
        circle_response = response
        response = circle_response.data
    if isinstance(response, list):
        return [convert_to_circle_object(r, api_key) for r in response]
    else:
        return response
