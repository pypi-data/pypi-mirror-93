import maglev
import shoppingcart

from typing import Any, List, Callable

class ShoppingCart:
	"""
	An Shopping Cart Library
	Add items and show a summary at checkout
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = shoppingcart.shoppingcart_ShoppingCart(bus)

	def Create(self, storeId: str) -> str:
		"""		Create a new shopping cart
		Args:
			storeId (str):
		Returns:
			cartId
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [storeId]
		ret = None
		def Create_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.Create', args, Create_Ret)
		return ret

	def AddItem(self, cartId: str, itemId: str, qty: float, price: float) -> float:
		"""		Add an item to a cart
		Args:
			cartId (str):
			itemId (str):
			qty (float):quantity
			price (float):price
		Returns:
			cart item index
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId, itemId, qty, price]
		ret = None
		def AddItem_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.AddItem', args, AddItem_Ret)
		return ret

	def ListItems(self, cartId: str) -> List[Any]:
		"""		Get a list of items in a cart
		Args:
			cartId (str):
		Returns:
			array of item objects
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId]
		ret = None
		def ListItems_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.ListItems', args, ListItems_Ret)
		return ret

	def RemoveItem(self, cartId: str, idx: float):
		"""		Remove an item from a cart
		Args:
			cartId (str):
			idx (float):item index
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId, idx]
		ret = None
		def RemoveItem_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.RemoveItem', args, RemoveItem_Ret)

	def UpdateQty(self, cartId: str, idx: float, qty: float):
		"""		Update cart item quantity
		Args:
			cartId (str):
			idx (float):item index
			qty (float):quantity
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId, idx, qty]
		ret = None
		def UpdateQty_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.UpdateQty', args, UpdateQty_Ret)

	def CountItems(self, cartId: str) -> float:
		"""		Count the items in a cart
		Args:
			cartId (str):
		Returns:
			number of items
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId]
		ret = None
		def CountItems_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.CountItems', args, CountItems_Ret)
		return ret

	def GetCartSummary(self, cartId: str) -> object:
		"""		Get a summary for a shopping cart
		Args:
			cartId (str):
		Returns:
			summary
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId]
		ret = None
		def GetCartSummary_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.GetCartSummary', args, GetCartSummary_Ret)
		return ret

	def Clear(self, cartId: str):
		"""		Clear all items from a shopping cart
		Args:
			cartId (str):
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [cartId]
		ret = None
		def Clear_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('ShoppingCart.Clear', args, Clear_Ret)



