from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from pgvector.django import HnswIndex, VectorField


# Create your models here.
class Injured(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20
    )  # We are going to apply a filter for text here
    cedula = models.CharField(max_length=16)
    genero = models.CharField(max_length=10)  # Filtro aqui tambien
    edad = models.IntegerField()
    ciudad = models.CharField(max_length=50)
    zona = models.CharField(max_length=400)
    ultimo_lugar = models.CharField(max_length=400)
    descripcion = models.CharField(max_length=500)
    foto_url = models.CharField()
    menor = models.BooleanField()
    origen = models.CharField()
    verificado = models.BooleanField()
    verificado_por = models.CharField()
    verificado_at = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    embedded = VectorField(dimensions=1536, null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            HnswIndex(
                name="injured_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            ),
            GinIndex(fields=["search_vector"], name="injured_search_gin"),
            models.Index(fields=["status"]),
            models.Index(fields=["zona"]),
            models.Index(fields=["verificado"]),
        ]
