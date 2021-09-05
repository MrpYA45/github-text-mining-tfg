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

""" Outcome class module.
"""

import json
from typing import List, Optional

from gtmcore.data.db.err import (OutcomeAlreadyExistsError,
                                 OutcomeNotExistsError)
from gtmcore.data.db.results.outcome import Outcome
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Outcomes():
    """ Class responsible of table-level outcome operations for Outcome.
    """
    @staticmethod
    def create(session: Session,
               task_id: int,
               repo_dir: str,
               model_type: str,
               outcome_data: dict,
               exec_time: float) -> Outcome:
        """ Creates a new Outcome record.

        Args:
            session (Session): The database session.
            task_id (int): The task id.
            repo_dir (str): The task repository.
            model_type (str): The model type.
            outcome_data (dict): The task outcome.
            exec_time (float): The task execution time.

        Raises:
        Raises:
            ValueError: Thrown when missing task_id, repo_dir,
                model_type, outcome_data or exec_time.
            OutcomeAlreadyExistError:
                Thrown when already exists a outcome with the same task_id.

        Returns:
            Outcome: The outcome.
        """
        if (task_id is None or not repo_dir or
                not model_type or outcome_data is None or exec_time is None):
            raise ValueError(
                "You cannot create an outcome without a task_id, a repo_dir, "
                "a model_type, an outcome_data and an exec_time.")
        try:
            outcome_data_str: str = json.dumps(outcome_data)
            outcome: Outcome = Outcome(
                task_id, repo_dir, model_type, outcome_data_str, exec_time)
            session.add(outcome)
            session.commit()
            return outcome
        except IntegrityError as err:
            session.rollback()
            raise OutcomeAlreadyExistsError from err

    @staticmethod
    def get_outcome(session: Session, task_id: int) -> Outcome:
        """ Gets a Outcome record from the repository.

        Args:
            session (Session): The database session.
            task_id (int): The task id.

        Raises:
            OutcomeNotExistsError:
                Thrown when there isn't any outcome with that task_id in the database records.

        Returns:
            Outcome: The outcome.
        """
        query: Query = session.query(Outcome).filter_by(task_id=task_id)
        outcome: Optional[Outcome] = query.first()
        if outcome is None:
            raise OutcomeNotExistsError
        return outcome

    @staticmethod
    def get_outcomes(session: Session,
                     repo_dir: str = None,
                     model_type: str = None) -> List[Outcome]:
        """ Gets a list of outcomes.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The outcome repository. Defaults to None.
            model_type (str, optional): The model type. Defaults to None.

        Returns:
            List[Outcome]: List of outcomes.
        """
        query: Query = session.query(Outcome)
        if repo_dir:
            query = query.filter_by(repo_dir=repo_dir)
        if model_type:
            query = query.filter_by(model_type=model_type)
        return query.all()
