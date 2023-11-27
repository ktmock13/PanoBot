def _safe_access(array, index):
  try:
      return array[index]
  except IndexError:
      return " "