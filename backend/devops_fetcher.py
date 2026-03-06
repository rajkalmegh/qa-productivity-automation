query = {
    "query": """
    SELECT [System.Id]
    FROM WorkItems
    WHERE
        [System.WorkItemType] = 'Bug'
        AND [System.State] NOT IN
            ('Rejected','Draft','Changes Required','Changes Done')
        AND [Custom.IssueSource] NOT IN
            ('CAT Audit','Employee Feedback')
        AND [System.CreatedBy] IN
            (
            'Supriya.Mohite',
            'Shriya.Patkar',
            'Rushikesh1.B',
            'Shweta.Kaware',
            'Prachi.Bagkar',
            'Medisetti.Sahitya',
            'Mihir.Sonar',
            'Nilesh2.Raut',
            'Amish.Shetty',
            'Vanshika.Darji',
            'Bhargav.Barvaliya',
            'Natasha.Jain',
            'Tarun.Eluri',
            'Asgar.Alam',
            'Sonia.Chawan',
            'Mahesh.Rayate',
            'Praphullakumar.L',
            'Pradnya.Chavan',
            'Abhishek55.S',
            'Ananya.Pahariya',
            'Ruturaj.Kalmegh',
            'Harshad.Bhalerao',
            'Harsh4.Dubey',
            'Kashish.Beotra'
            )
        AND [Microsoft.VSTS.Common.CreatedDate] >= '2025-04-01'
        AND [Microsoft.VSTS.Common.CreatedDate] < @StartOfDay
    """
}
