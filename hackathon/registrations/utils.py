from hackathon.registrations.models import Registrations


def amount(team: Registrations):
    team.team_members = len(team.team.all()) + 1
    team.save()
    return team.team_members * 300 * 100
