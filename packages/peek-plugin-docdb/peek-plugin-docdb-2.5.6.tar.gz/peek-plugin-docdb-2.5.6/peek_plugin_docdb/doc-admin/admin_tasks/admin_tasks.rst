Admin Tasks
-----------

This section describes how to perform administration tasks for the Document DB plugin.

Updating Document Types
```````````````````````

The document type names displayed to the user can be update via the admin UI.
To update the names, follow this procedure:

----

#.  Open the Peek Admin UI and navigate to the DocumentDB plugin.

#.  Click on the **Edit Document Types** tab

#.  Update the **Description** column.

#.  Click save.

.. image:: admin_task_update_document_types.png

----

The user will see the updated document type name when next they view the document.

Updating Property Names
```````````````````````

The property names displayed to the user can be updated via the admin UI.
To update the names, follow this procedure:

----

#.  Open the Peek Admin UI and navigate to the DocumentDB plugin.

#.  Click on the **Edit Property Names** tab

#.  Update the **Title** column.

#.  Click save.


.. image:: admin_task_update_property_name.png

----

The user will see the updated property name when next they view the document.

Recompile Index
```````````````

The admin task recompiles the document index for a given model set.

The documents are stored in one of 8192 hash buckets.
Recompiling the index will rebuild these bash buckets.

Each model set has it's own document index.

.. note:: You should not expect to need to recompile the index.

----

#.  Find the ID of the model set to recompile the index for.

#.  Stop all peek services

#.  Execute the following, replacing <ID> with the :code:`modeSetId` ::


        -- Delete the existing index data.
        DELETE FROM pl_docdb."DocDbChunkQueue" WHERE "modelSetId" = <ID>;
        DELETE FROM pl_docdb."DocDbEncodedChunkTuple" WHERE "modelSetId" = <ID>;

        -- Queue the chunks for compiling.
        INSERT INTO pl_docdb."DocDbChunkQueue" ("modelSetId", "indexBucket")
        SELECT DISTINCT "modelSetId", "indexBucket"
        FROM pl_docdb."DocDbDocument"
        WHERE "modelSetId" = <ID>;


#.  Start all Peek services

----

Peek will now rebuild the document index for that model set.