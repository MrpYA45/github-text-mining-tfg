# Copyright (C) 2021 Pablo Fernández Bravo
#
# This file is part of github-text-mining-tfg.
#
# github-text-mining-tfg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# github-text-mining-tfg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with github-text-mining-tfg.  If not, see <http://www.gnu.org/licenses/>.

""" Comments class module.
"""

from typing import List, Optional

from gtmcore.data.db.err import (CommentAlreadyExistsError,
                                 CommentNotExistsError)
from gtmcore.data.db.results.comment import Comment
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Comments():
    """ Class responsible of table-level comments operations for Comments.
    """
    @staticmethod
    def create(session: Session,
               repo_dir: str,
               issue_id: int,
               comment_id: int,
               author: str,
               body: str) -> Comment:
        """ Creates a new Comment record.

        Args:
            session (Session): The database session.
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            comment_id (int): The comment identifier.
            author (str): The comment author.
            body (str): The comment body.

        Raises:
            ValueError: Thrown when missing repo_dir, issue_id, comment_id or author.
            CommentAlreadyExistError:
                Thrown when already exists a comment with the same repo_dir,
                issue_id and comment_id.

        Returns:
            Comment: The comment.
        """
        if not repo_dir or issue_id is None or comment_id is None or not author:
            raise ValueError(
                "You cannot create an issue without a repo_dir, "
                "an issue_id, a comment_id and an author.")
        try:
            comment: Comment = Comment(
                repo_dir, issue_id, comment_id, author, body)
            session.add(comment)
            session.commit()
            return comment
        except IntegrityError as err:
            session.rollback()
            raise CommentAlreadyExistsError from err

    @staticmethod
    def get_comment(session: Session, repo_dir: str, issue_id: int, comment_id: int) -> Comment:
        """ Gets a Comment record from the repository.

        Args:
            session (Session): The database session.
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            comment_id (int): The comment identifier.

        Raises:
            CommentNotExistsError:
                Thrown when there isn't any comment with that
                repo_dir, issue_id and comment_id in the database records.

        Returns:
            Comment: The comment.
        """
        query: Query = session.query(Comment).filter_by(
            repo_dir=repo_dir, issue_id=issue_id, comment_id=comment_id)
        comment: Optional[Comment] = query.first()
        if comment is None:
            raise CommentNotExistsError
        return comment

    @staticmethod
    def get_comments(session: Session,
                     repo_dir: str = None,
                     issue_id: int = None,
                     author: str = None) -> List[Comment]:
        """ Gets a list of comments.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The issue repository. Defaults to None.
            issue_id (int, optional): The comment identifier. Defaults to None.
            author (str, optional): The comments author. Defaults to None.

        Returns:
            List[Comment]: List of comments.
        """
        query: Query = session.query(Comment)
        if repo_dir:
            query = query.filter_by(repo_dir=repo_dir)
        if issue_id:
            query = query.filter_by(issue_id=issue_id)
        if author:
            query = query.filter_by(author=author)
        return query.all()
