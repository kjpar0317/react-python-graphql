import strawberry
from typing import Optional, Dict, Any
import datetime

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import select, and_
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.types.base_scalars import DateTime

from . import models
from .utils import IsAuthenticated, signJWT


@strawberry.type
class AuthData:
    user_id: strawberry.ID
    token: Optional[str] = None
    token_expiration: Optional[float] = 0

    @classmethod
    def marshal(cls, model: Dict) -> "AuthData":
        return cls(user_id=strawberry.ID(model["user_id"]), token=model["token"], token_expiration=model["token_expiration"])


@strawberry.type
class CodeM:
    C_ID: strawberry.ID
    C_PARENT_ID: Optional[str] = None
    C_NAME: Optional[str] = None
    C_ENG_NAME: Optional[str] = None
    C_DESCRIPTION: Optional[str] = None

    # @strawberry.field
    # async def code_problems(self, info: Info) -> list["CodeProblem"]:
    #     code_problems = await info.context["codeProblems_by_codeM"].load(self.C_ID)
    #     print(code_problems)
    #     return [CodeProblem.marshal(problem) for problem in code_problems]

    @classmethod
    def marshal(cls, model: models.CodeM) -> "CodeM":
        return cls(C_ID=strawberry.ID(model.C_ID), C_PARENT_ID=model.C_PARENT_ID, C_NAME=model.C_NAME, C_ENG_NAME=model.C_ENG_NAME, C_DESCRIPTION=model.C_DESCRIPTION)


@strawberry.type
class CodeProblem:
    CP_SEQ: strawberry.ID
    CP_CATEGORY_CD: str
    CP_TITLE: str
    CP_LEVEL_CD: str
    CP_CONTENT: Optional[str] = None
    CP_TAG: Optional[str] = None
    CP_LAPTIME: DateTime = datetime.datetime.now()

    @classmethod
    def marshal(cls, model: models.CodeProblem) -> "CodeProblem":
        return cls(
            CP_SEQ=strawberry.ID(str(model.CP_SEQ)),
            CP_CATEGORY_CD=model.CP_CATEGORY_CD,
            CP_TITLE=model.CP_TITLE,
            CP_LEVEL_CD=model.CP_LEVEL_CD,
            CP_CONTENT=model.CP_CONTENT,
            CP_TAG=model.CP_TAG,
            CP_LAPTIME=model.CP_LAPTIME
        )


@strawberry.type
class Query:
    # @strawberry.field
    # async def login(self, email: str, password: str):
    #     return "hello"

    @strawberry.field
    # @strawberry.field(permission_classes=[IsAuthenticated])
    async def codes(self, page: Optional[int] = 1, page_size: Optional[int] = 100) -> list[CodeM]:
        async with models.get_session() as s:
            sql = select(models.CodeM).order_by(
                models.CodeM.C_ID).offset((page - 1) * page_size).limit(page_size)
            codes = (await s.execute(sql)).scalars().all()
            return [CodeM.marshal(code) for code in codes]

    @strawberry.field
    async def code_problems(self, page: Optional[int] = 1, page_size: Optional[int] = 100) -> list[CodeProblem]:
        async with models.get_session() as s:
            sql = select(models.CodeProblem).order_by(
                models.CodeProblem.CP_SEQ).offset((page - 1) * page_size).limit(page_size)
            # code_problems = (await s.execute(sql)).scalars().unique().all()
            code_problems = (await s.execute(sql)).scalars().all()
            return [CodeProblem.marshal(problem) for problem in code_problems]


@strawberry.type
class Mutation:
    @ strawberry.mutation
    async def login(self, id: str, password: str) -> AuthData:
        async with models.get_session() as s:
            info = None

            sql = select(models.Users).where(
                and_(models.Users.id == id, models.Users.password == password))

            user = (await s.execute(sql)).scalars().first()

            if user is not None:
                print(user.id)
                info = AuthData.marshal(signJWT(user.id))
            else:
                raise HTTPException("없는 유저입니다.")
                # return NotExistUser()
        return info

    @strawberry.mutation
    async def add_code(self, C_ID: str, C_PARENT_ID: Optional[str], C_NAME: Optional[str], C_ENG_NAME: Optional[str], C_DESCRIPTION: Optional[str]) -> CodeM:
        async with models.get_session() as s:
            code = None

            sql = select(models.CodeM).where(
                and_(models.CodeM.C_ID == C_ID, models.CodeM.C_PARENT_ID == C_PARENT_ID))
            code = (await s.execute(sql)).scalars().first()

            if code is None:
                raise HTTPException("중복 유저입니다.")

            insert_code = models.CodeM(C_ID=C_ID, C_PARENT_ID=C_PARENT_ID,
                                       C_NAME=C_NAME, C_ENG_NAME=C_ENG_NAME, C_DESCRIPTION=C_DESCRIPTION)
            s.add(insert_code)
            await s.commit()
        return CodeM.marshal(insert_code)

    @strawberry.mutation
    async def add_code_problem(self, CP_CATEGORY_CD: str, CP_TITLE: str, CP_LEVEL_CD: str, CP_CONTENT: Optional[str], CP_TAG: Optional[str]) -> CodeProblem:
        async with models.get_session() as s:
            code_problem = models.CodeProblem(
                CP_CATEGORY_CD=CP_CATEGORY_CD, CP_TITLE=CP_TITLE, CP_LEVEL_CD=CP_LEVEL_CD, CP_CONTENT=CP_CONTENT, CP_TAG=CP_TAG)
            s.add(code_problem)
            await s.commit()
        return CodeProblem.marshal(code_problem)

# async def load_codeProblems_by_code(keys: list) -> list[CodeProblem]:
#     async with models.get_session() as s:
#         all_queries = [select(CodeM).where(
#             CodeM.C_ID == key) for key in keys]
#         print(all_queries)
#         data = [(await s.execute(sql)).scalars().unique().all() for sql in all_queries]
#         print(keys, data)
#     return data


# async def get_context() -> dict:
#     return {
#         "codeProblems_by_code": DataLoader(load_fn=load_codeProblems_by_code),
#     }

# schema = strawberry.Schema(query=Query)
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
# graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(graphql_app, prefix="/graphql")
