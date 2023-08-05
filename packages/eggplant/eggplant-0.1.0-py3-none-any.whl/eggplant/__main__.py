import fastapi as f
import sqlalchemy as s
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import pathlib
import royalnet.scrolls as rs
import pydantic
import uvicorn
import pkg_resources


scroll = rs.Scroll.from_file("EGGPLANT", file_path=pathlib.Path("config.toml"))
engine = sqlalchemy.create_engine(scroll["database.url"])
Base = sqlalchemy.ext.declarative.declarative_base(bind=engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
app = f.FastAPI(title="Eggplant",
                description="Reactions as-a-service",
                version=pkg_resources.get_distribution("eggplant").version)


class ReactionT(Base):
    __tablename__ = "reaction"

    uri = s.Column(s.String, primary_key=True)
    namespace = s.Column(s.String, primary_key=True)
    reaction = s.Column(s.String, primary_key=True)
    count = s.Column(s.Integer, nullable=False, default=0, server_default="0")


class ReactionM(pydantic.BaseModel):
    uri: str
    namespace: str
    reaction: str
    count: str

    class Config(pydantic.BaseConfig):
        orm_mode = True


@app.get("/", response_model=list[ReactionM],
         summary="Get all reactions for a resource.")
def get(uri: str, namespace: str):
    session: sqlalchemy.orm.Session = Session()
    reactions: list[ReactionT] = session.query(ReactionT).filter_by(uri=uri, namespace=namespace).all()
    return reactions


@app.post("/", response_model=ReactionM,
          summary="Add a new reaction to a resource.")
def post(uri: str, namespace: str, reaction: str):
    session: sqlalchemy.orm.Session = Session()
    session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
    r = session.query(ReactionT).filter_by(uri=uri, namespace=namespace, reaction=reaction).one_or_none()
    if r is None:
        r = ReactionT(uri=uri, namespace=namespace, reaction=reaction)
        session.add(r)
        session.commit()
    r.count += 1
    session.commit()
    return r


if __name__ == "__main__":
    Base.metadata.create_all()
    uvicorn.run(app, port=scroll.get("api.port", default=30020))
