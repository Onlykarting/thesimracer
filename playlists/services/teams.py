from playlists.models import Team
from django.contrib.auth.models import User
from playlists.services.exceptions import UniqueConstraint
from typing import Optional


def create_team(creator: User, team_name: str):
    """
    Creates team with `team_name` name and makes creator host of it.
    If team_name has been already taken, raises UniqueConstraint.
    :param creator:
    :param team_name:
    :return:
    """
    # Check if no team with the team_name exists.
    if Team.objects.filter(name=team_name).exists():
        raise UniqueConstraint("Team already exists.")

    team = Team(name=team_name, host=creator)
    team.members.add(creator)


def transfer_host_privileges(team: Team, to_user: User):
    """
    Transfers host privileges from team host to user.
    If the user isn't in the team, they will be added to it.
    If the team host and user are the same, nothing will be done.
    :param team:
    :param to_user:
    :return: None
    """
    if team.host == to_user:
        return

    team.host = to_user
    if to_user not in team.members:
        team.members.add(to_user)
    team.save()


def add_user_to_team(user: User, team: Team):
    """
    Adds the user to team.
    If the user is already in the team, nothing will be done.
    :param user:
    :param team:
    :return: None
    """
    if user in team.members:
        team.members.add(user)
        team.save()


def remove_user_from_team(user: User, team: Team, transfer_host_to: Optional[User] = None):
    """
    Removes the user from the team.
    If the user isn't in the team, nothing will be done.
    If the user is host:
      . if :transfer_host_to: is specified and isn't the same with host,
        privileges will be transferred to `transfer_host_to`.
      . if :transfer_host_to: is not specified and host is not sole member of the team,
        privileges will be transferred to undefined (random) member of the team.
      . if host is sole member of the team, the team will be automatically removed.
    :param transfer_host_to: member who will receive host privileges, if user is host. Must be member of the team.
    :param user:
    :param team:
    :return:
    """
    if user not in team.members:
        return

    if transfer_host_to is not None and transfer_host_to not in team.members:
        raise ValueError("transfer_host_to must be a part of the team.")

    if user != team.host:

        team.members.remove(user)
        team.save()

    else:

        team.members.remove(user)

        if len(team.members) < 1:

            team.delete()

        elif transfer_host_to is not None:

            team.host = transfer_host_to

        else:

            # Randomly choosing new host
            team.host = team.members[0]

        team.save()


def is_host_of_team(user: User, team: Optional[Team] = None, team_id: Optional[int] = None) -> bool:
    """
    Checks if the user is host of the team.
    Team must be specified via object type of Team or team id.
    Any of `team` and `team_id` parameters must be specified, but not both.
    :param user:
    :param team:
    :param team_id:
    :return: true, if user is host of the team, else false
    """
    if team is None and team_id is None:
        raise ValueError("Neither `team` nor `team_id` params haven't been specified.")

    if team is not None and team_id is not None:
        raise ValueError("`team` and `team_id` can't be specified at the same time.")

    if team is not None:
        return Team.objects.filter(host=user, team_id=team.pk).exists()

    if team_id is not None:
        return Team.objects.filter(host=user, team_id=team_id).exists()


def is_member_of_team(user: User, team: Optional[Team] = None, team_id: Optional[int] = None) -> bool:
    """
    Checks if the user is member of the team.
    Team must be specified via object type of Team or team id.
    Any of `team` and `team_id` parameters must be specified, but not both.
    :param user:
    :param team:
    :param team_id:
    :return: true, if user is member of the team, else false
    """
    if team is None and team_id is None:
        raise ValueError("Neither `team` nor `team_id` params haven't been specified.")

    if team is not None and team_id is not None:
        raise ValueError("`team` and `team_id` can't be specified at the same time.")

    if team is not None:
        return Team.objects.filter(members=user, team_id=team.pk).exists()

    if team_id is not None:
        return Team.objects.filter(members=user, team_id=team_id).exists()


def delete_team(team: Team):
    """
    Deletes team. This function is useless now.
    But business-logic changing will require only changing this function.
    :param team: team to be deleted.
    :return: None
    """
    team.delete()
