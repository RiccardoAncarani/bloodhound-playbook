MATCH (g:GPO) WITH g
MATCH (g)<-[a]-(u)
WHERE toInteger(split(u.objectsid,'-')[7])>1000
RETURN g.name, type(a) ,u.name, u.objectsid
