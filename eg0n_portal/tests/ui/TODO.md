Token create
token delete
token view
token view list
token modify -> forbidden
group create
group view
grou plist view
group delete
group modify
cambio password


users:
CREATE -> admin
EDIT -> admin, staff in the same group
    staff cannot delete/edit admins
    staff cannot set a group different than the shared ones
    staff cannot edit staff

Check self cannot modify privileges fur users and staff
