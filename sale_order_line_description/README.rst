===========================
Sale order line description
===========================


This module sets the description to company's own rule: "attribute_name: attribute_value" on the sale order
lines, instead of "Ref+Name+Sale Description". Also it sets the description on Order Lines invisible to avoid clutter.

**Table of contents**

.. contents::
   :local:

Configuration
=============

The user has to belong to group_use_product_description_per_so_line.
This is possible by selecting the related option in the following menu:

* *Sales > Settings > Quotations & Orders > Product Sale Description*

Usage
=====

#. Go to **Sales > Settings > Quotations & Orders** and check "Product Sale
   description* to use only product sale description on the sales order lines.
#. Go to **Setting > Users & Companies > Users** and check you have checked
   the "Use only product purchase description on order lines" access right for
   your user.
#. Add or modify a sale description to any of your products.
#. Create a sale order and add a sale order line with this product and check
   out that now sale order line description only contains the sale description
   you entered.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/sale-workflow/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/sale-workflow/issues/new?body=module:%20sale_order_line_description%0Aversion:%2012.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Agile Business Group

Contributors
~~~~~~~~~~~~

* Alex Comba <alex.comba@agilebg.com>
* Daniel Campos <danielcampos@avanzosc.es>
* Simone Rubino <simone.rubino@agilebg.com>
* `Tecnativa <https://www.tecnativa.com>`_ :

  * Vicent Cubells

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/sale-workflow <https://github.com/OCA/sale-workflow/tree/12.0/sale_order_line_description>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
