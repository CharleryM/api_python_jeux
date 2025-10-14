"""
games CRUD
"""

from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

router = APIRouter()

class Game(BaseModel):
    """Modèle de données pour un jeu vidéo"""
    id: int = Field(..., description="Identifiant unique du jeu")
    title: str = Field(..., min_length=1, max_length=200, description="Titre du jeu")
    editor: str = Field(..., min_length=1, max_length=100, description="Editeur du jeu")
    available: bool = Field(..., description="Disponibilité du jeu")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "smash bros melee",
                "editor": "Nintendo",
                "available": True,
                "created_at": "2023-10-01T12:00:00",
                "updated_at": "2023-10-01T12:00:00",
            }
        }
    )
    
class GameUpdate(BaseModel):
    """
    chéma pour mettre à jour un jeu.
    ous les champs sont optionnels (on peut modifier seulement certains champs).
    """
    itle: Optional[str] = Field(None, min_length=1, max_length=200)
    editor: Optional[str] = Field(None, min_length=1, max_length=100)
    available: Optional[bool] = Field(None, description="Disponibilité du jeu")

class addGame(Game):
    """ajout d'un jeu"""
    id: int
    created_at: datetime
    updated_at: datetime
    
class gameCreate(BaseModel):
    """création d'un jeu"""
    title: str = Field(..., min_length=1, max_length=200, description="Titre du jeu")
    editor: str = Field(..., min_length=1, max_length=100, description="Editeur du jeu")
    available: bool = Field(default=True, description="Disponibilit du jeu")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Date de cration du jeu")

class UpdateGame(BaseModel):
    """modification d'un jeu"""
    id: int = Field(..., description="Identifiant unique du jeu")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Titre du jeu")
    editor: Optional[str] = Field(None, min_length=1, max_length=100, description="Editeur du jeu")
    available: Optional[bool] = Field(None, description="Disponibilité du jeu")
    created_at: Optional[datetime] = Field(None, description="Date de création du jeu")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Date de mise à jour du jeu")

class game(Game):
    """détail d'un jeu prcis"""
    id: int
    created_at: datetime
    available: bool
    updated_at: datetime

    id: int = Field(..., description="Identifiant unique du jeu")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "smash bros melee",
                "editor": " Nintendo",
                "available": True,
            }
        }
    )
    
games_db: List[dict] = [
    {
        "id": 0,
        "title": "The Legend of Zelda: Ocarina of Time",
        "editor": "Nintendo",
        "available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": 1,
        "title": "Super Mario 64", 
        "editor": "Nintendo",
        "available": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": 2,
        "title": "Final Fantasy VII",
        "editor": "Square Enix",
        "available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
]
NEXT_ID = len(games_db)
    
def looking_for_game(id: int):
    """Cherche un jeu par son ID"""
    for game in games_db:
        if game.id == id:
            return game
    return None

def find_game_by_editor(game_editor: str)->Optional[dict]:
    """
    Recherche un jeu par son éditeur
    Args:
        game_editor(string):L'identifiant
    Return:
    Optional[dict]:jeu si trouvé, None sinon
    """
    for game in games_db:
        if game["editor"]==game_editor:
            return game
    return None

@router.get("/", response_model=List[game], status_code=status.HTTP_200_OK)
async def get_all_games(available: Optional[bool] = None, editor: Optional[str] = None):
    """
    Récupère la liste de tous les jeux.

    Paramètres de filtrage optionnels :
    - available: Filtrer par disponibilité (true/false)
    - editor: Filtrer par auteur (recherche partielle, insensible à la casse)

    Returns:
        Liste des jeux correspondant aux critères
    """
    result = games_db.copy()

    if available is not None:
        result = [game for game in result if game["available"] == available]

    if editor:
        result = [game for game in result if editor.lower() in game["editor"].lower()]
        
    return result

@router.get("/", response_model=List[game], status_code=status.HTTP_200_OK)
async def get_all_games(available: Optional[bool] = None, editor: Optional[str] = None):
    """
    Récupère la liste de tous les jeux.

    Paramètres de filtrage optionnels :
    - available: si le jeu est en stock (true/false)
    - editor: Filtrer par auteur (recherche partielle, insensible à la casse)

    Returns:
        Liste des jeux correspondant aux critères
    """
    result = games_db.copy()


    if available is not None:
        result = [game for game in result if game["available"] == available]

    if editor:
        result = [game for game in result if editor.lower() in game["editor"].lower()]

    return result

@router.get("/{game_id}", response_model=Game, status_code=status.HTTP_200_OK)
async def get_game(game_id: int):
    """
    Récupère les détails d'un jeu spécifique par son ID.

    Args:
        game_id: L'identifiant du jeu

    Returns:
        Les informations complètes du jeu

    Raises:
        HTTPException 404: Si le jeu n'existe pas
    """
    game = find_game_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Le jeu avec l'ID {game_id} n'existe pas",
        )
    return Game(**game)

def find_game_by_id(game_id: int)->Optional[dict]:
    """
    Recherche un jeu par son ID
    Args:
        game_id(int):L'identifiant
    Return:
    Optional[dict]:jeu si trouvé, None sinon
    """
    for game in games_db:
        if game["id"]==game_id:
            return game
    return None

def find_game_by_editor(game_editor: str)->Optional[dict]:
    """
    Recherche un jeu par son éditeur
    Args:
        game_editor(int):L'identifiant
    Return:
    Optional[dict]:jeu si trouvé, None sinon
    """
    for game in games_db:
        if game["editor"]==game_editor:
            return game
    return None

@router.get("/", response_model=List[Game], status_code=status.HTTP_200_OK)
async def get_all_games(available: Optional[bool] = None, editor: Optional[str] = None):
    """
    Récupère la liste de tous les jeux.

    Paramètres de filtrage optionnels :
    - available: Filtrer par disponibilité (true/false)
    - editor: Filtrer par auteur (recherche partielle, insensible à la casse)

    Returns:
        Liste des jeux correspondant aux critères
    """
    result = games_db.copy()


    if available is not None:
        result = [game for game in result if game["available"] == available]

    if editor:
        result = [game for game in result if editor.lower() in game["editor"].lower()]


    return result

@router.get("/{game_id}", response_model=Game, status_code=status.HTTP_200_OK)
async def get_game(game_id: int):
    """
    Récupère les détails d'un jeu spécifique par son ID.

    Args:
        game_id: L'identifiant du jeu

    Returns:
        Les informations complètes du jeu

    Raises:
        HTTPException 404: Si le jeu n'existe pas
    """
    game = find_game_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Le jeu avec l'ID {game_id} n'existe pas",
        )

    return game

@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_game(game: gameCreate):
    """
    ajoute un nouveau jeu dan le stock.

    Args:
        game: Les informations du jeu à créer

    Returns:
        Le jeu créé avec son ID et sa date de création

    Raises:
        HTTPException 400: Si un jeu avec le même éditeur existe déjà
    """
    global NEXT_ID

    existing_game = find_game_by_editor(game.editor)
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Un jeu avec l'éditeur {game.editor} existe déjà (ID: {existing_game['id']})",
        )

    new_game = {
        "id": NEXT_ID,
        **game.model_dump(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    games_db.append(new_game)
    NEXT_ID += 1
    return Game(**new_game)

@router.put("/{game_id}", response_model=game, status_code=status.HTTP_200_OK)
async def update_game(game_id: int, game_update: GameUpdate):
    """
    Met à jour les informations d'un jeu existant.
    Seuls les champs fournis sont modifiés.

    Args:
        game_id: L'identifiant du jeu à modifier
        game_update: Les champs à mettre à jour

    Returns:
        Le jeu mis à jour

    Raises:
        HTTPException 404: Si le jeu n'existe pas
        HTTPException 400: Si l'editor modifié existe déjà sur un autre jeu
    """
    game = find_game_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Le jeu avec l'ID {game_id} n'existe pas",
        )

    update_data = game_update.model_dump(exclude_unset=True)
    if "editor" in update_data:
        existing_game = find_game_by_editor(update_data["editor"])
        if existing_game and existing_game["id"] != game_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Un autre jeu utilise déjà l'editor {update_data['editor']}",
            )

    game.update(update_data)
    
@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: int):
    """
    Supprime un jeu de la bibliothèque.

    Args:
        game_id: L'identifiant du jeu à supprimer

    Returns:
        Aucun contenu (code 204)

    Raises:
        HTTPException 404: Si le jeu n'existe pas
    """
    game = find_game_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Le jeu avec l'ID {game_id} n'existe pas",
        )

    games_db.remove(game)
    return None